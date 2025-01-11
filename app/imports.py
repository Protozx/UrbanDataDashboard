from flask import render_template, redirect, url_for, flash, request, abort, send_from_directory, session,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import app, bcrypt, get_db
from .models import User
import random, os, json
from datetime import datetime

from app.scripts.Reporter import statistics_pdf
from app.scripts.Cleaner import proccessed_pdf

DATASET_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datasets')
REPORT_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
PROCESSED_DIRECTORY = os.path.join(DATASET_DIRECTORY, 'processed')


if not os.path.exists(DATASET_DIRECTORY):
    os.makedirs(DATASET_DIRECTORY)
if not os.path.exists(REPORT_DIRECTORY):
    os.makedirs(REPORT_DIRECTORY)
if not os.path.exists(PROCESSED_DIRECTORY):
    os.makedirs(PROCESSED_DIRECTORY)