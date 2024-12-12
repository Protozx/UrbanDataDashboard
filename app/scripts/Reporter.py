import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo

import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

class ReportGenerator:
    def __init__(self, title, csv_input_path, pdf_output_path):
        self.title = title
        self.csv_input_path = csv_input_path
        self.pdf_output_path = pdf_output_path
        
        # Cargar datos con un encoding compatible
        self.df = pd.read_csv(self.csv_input_path, encoding='latin-1')
        # Intentamos que todas las columnas numéricas se conviertan a float si posible
        for c in self.df.columns:
            try:
                self.df[c] = self.df[c].str.strip()  # Eliminar espacios
                self.df[c] = self.df[c].replace(',', '.', regex=True)  # En caso de decimales con coma
                self.df[c] = pd.to_numeric(self.df[c], errors='coerce')
            except:
                pass
        
        self.styles = getSampleStyleSheet()
        self.style_title = self.styles['Title']
        self.style_normal = self.styles['BodyText']
        self.style_heading = self.styles['Heading2']
        
        self.elements = []
        
    def generate_report(self):
        doc = SimpleDocTemplate(self.pdf_output_path, pagesize=A4)
        
        self.elements.append(Paragraph(self.title, self.style_title))
        self.elements.append(Spacer(1, 12))
        
        self._add_general_summary()
        
        for col in self.df.columns:
            self._add_variable_section(col)
        
        doc.build(self.elements)
        
    def _add_general_summary(self):
        self.elements.append(Paragraph("Resumen estadístico general", self.style_heading))
        self.elements.append(Spacer(1, 12))
        
        for col in self.df.columns:
            desc = self.df[col].describe(include='all').dropna()
            
            self.elements.append(Paragraph(f"Resumen estadístico para '{col}'", self.style_heading))
            self.elements.append(Spacer(1, 12))
            
            data = [['Estadístico', 'Valor']]
            for idx, val in desc.items():
                data.append([idx, str(val)])
            
            t = Table(data, hAlign='LEFT')
            t.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0), colors.grey),
                ('TEXTCOLOR',(0,0),(-1,0), colors.whitesmoke),
                ('ALIGN',(1,1),(-1,-1),'RIGHT'),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX',(0,0),(-1,-1),0.25, colors.black),
            ]))
            
            self.elements.append(t)
            self.elements.append(Spacer(1, 24))
        
    def _add_variable_section(self, col):
        self.elements.append(PageBreak())
        self.elements.append(Paragraph(f"Variable: {col}", self.style_heading))
        self.elements.append(Spacer(1, 12))
        
        if pd.api.types.is_numeric_dtype(self.df[col]):
            self._add_numeric_variable_analysis(col)
        else:
            self._add_non_numeric_variable_analysis(col)
        
    def _add_numeric_variable_analysis(self, col):
        missing_count = self.df[col].isna().sum()
        total_count = len(self.df[col])
        
        self.elements.append(Paragraph("Valores faltantes:", self.style_normal))
        self.elements.append(Paragraph(f"{missing_count} de {total_count}", self.style_normal))
        self.elements.append(Spacer(1, 12))
        
        self._plot_missing_values(col)
        
        outliers_count = self._count_outliers(col)
        self.elements.append(Paragraph("Outliers:", self.style_normal))
        self.elements.append(Paragraph(f"Cantidad de outliers: {outliers_count}", self.style_normal))
        self.elements.append(Spacer(1, 12))
        
        self._plot_box(col, filename_suffix="_outliers")
        
        mean_val = self.df[col].mean()
        median_val = self.df[col].median()
        mode_val = self.df[col].mode().iloc[0] if not self.df[col].mode().empty else None
        
        self.elements.append(Paragraph("Tendencias:", self.style_normal))
        self.elements.append(Paragraph(f"Media: {mean_val}", self.style_normal))
        self.elements.append(Paragraph(f"Mediana: {median_val}", self.style_normal))
        self.elements.append(Paragraph(f"Moda: {mode_val}", self.style_normal))
        self.elements.append(Spacer(1, 12))
        
        self._plot_trends(col, mean_val, median_val, mode_val)
        
        var_val = self.df[col].var()
        self.elements.append(Paragraph("Varianza:", self.style_normal))
        self.elements.append(Paragraph(str(var_val), self.style_normal))
        self.elements.append(Spacer(1, 12))
        
    def _add_non_numeric_variable_analysis(self, col):
        missing_count = self.df[col].isna().sum()
        total_count = len(self.df[col])
        
        self.elements.append(Paragraph("Valores faltantes:", self.style_normal))
        self.elements.append(Paragraph(f"{missing_count} de {total_count}", self.style_normal))
        self.elements.append(Spacer(1, 12))
        
        value_counts = self.df[col].value_counts().head(5)
        self.elements.append(Paragraph("Valores más comunes:", self.style_normal))
        
        data = [["Categoría", "Frecuencia"]]
        for idx, val in value_counts.items():
            data.append([str(idx), str(val)])
        t = Table(data, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0), colors.whitesmoke),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX',(0,0),(-1,-1),0.25, colors.black),
        ]))
        self.elements.append(t)
        self.elements.append(Spacer(1, 12))
        
        self._plot_pie(col)
        
    def _plot_missing_values(self, col):
        fig, ax = plt.subplots()
        missing = self.df[col].isna().sum()
        not_missing = len(self.df[col]) - missing
        ax.bar(["Faltantes", "No faltantes"], [missing, not_missing], color=["red", "green"])
        ax.set_title("Valores faltantes")
        
        img_path = self._save_fig(col, "_missing")
        self.elements.append(Image(img_path, width=400, height=200))
        self.elements.append(Spacer(1, 12))
        plt.close(fig)
        
    def _count_outliers(self, col):
        q1 = self.df[col].quantile(0.25)
        q3 = self.df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5*iqr
        upper_bound = q3 + 1.5*iqr
        outliers = self.df[(self.df[col]<lower_bound) | (self.df[col]>upper_bound)][col]
        return outliers.count()
        
    def _plot_box(self, col, filename_suffix=""):
        fig, ax = plt.subplots()
        data = self.df[col].dropna()
        if len(data) > 0:
            ax.boxplot(data, vert=False)
        ax.set_title(f"Gráfica de caja para {col}")
        img_path = self._save_fig(col, filename_suffix+"_box")
        self.elements.append(Image(img_path, width=400, height=200))
        self.elements.append(Spacer(1, 12))
        plt.close(fig)
        
    def _plot_trends(self, col, mean_val, median_val, mode_val):
        fig, ax = plt.subplots()
        data = self.df[col].dropna()
        if len(data) > 0:
            ax.hist(data, bins=20, alpha=0.7, color='blue', edgecolor='black')
            if mean_val is not None:
                ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label='Media')
            if median_val is not None:
                ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label='Mediana')
            if mode_val is not None:
                ax.axvline(mode_val, color='orange', linestyle='--', linewidth=2, label='Moda')
            ax.set_title(f"Tendencias en {col}")
            ax.legend()
        
        img_path = self._save_fig(col, "_trends")
        self.elements.append(Image(img_path, width=400, height=200))
        self.elements.append(Spacer(1, 12))
        plt.close(fig)
        
    def _plot_pie(self, col):
        value_counts = self.df[col].value_counts().head(5)
        fig, ax = plt.subplots()
        if len(value_counts) > 0:
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Distribución de {col}")
        
        img_path = self._save_fig(col, "_pie")
        self.elements.append(Image(img_path, width=400, height=200))
        self.elements.append(Spacer(1, 12))
        plt.close(fig)
        
    def _save_fig(self, col, suffix=""):
        if not os.path.exists("temp_images"):
            os.makedirs("temp_images")
        
        img_path = os.path.join("temp_images", f"{col}{suffix}.png")
        plt.savefig(img_path, dpi=100, bbox_inches='tight')
        return img_path


def initialize_report(title, csv_name, dataset_directory, report_directory):
    dataset_path = os.path.join(dataset_directory, f"{csv_name}.csv") 
    report_path = os.path.join(report_directory, f"{csv_name}.pdf") 

    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    return ReportGenerator(title, dataset_path, report_path)

def borrar_contenido_carpeta(direccion):
    if os.path.isdir(direccion):
        for nombre in os.listdir(direccion):
            ruta_completa = os.path.join(direccion, nombre)
            try:
                if os.path.isdir(ruta_completa):
                    shutil.rmtree(ruta_completa)
                else:
                    os.remove(ruta_completa)
            except Exception as e:
                print(f"No se pudo eliminar {ruta_completa}. Razón: {e}")
    else:
        print("La dirección proporcionada no es una carpeta.")

def statistics_pdf(id, titulo, dataset_directory, report_directory):
    report = initialize_report(titulo + " de la isla", id, dataset_directory, report_directory)
    report.generate_report()
    borrar_contenido_carpeta("temp_images")
    
