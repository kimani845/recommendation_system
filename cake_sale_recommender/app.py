# Flask Main App
from flask import Flask, render_template, request, redirect, url_for, flash
from cake_sales_analysis import CakeSalesTracker, CAKE_TYPES, REGIONS
from recommender import generate_recommendations
from database import get_connection
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
tracker = CakeSalesTracker()

@app.route('/')
def index():