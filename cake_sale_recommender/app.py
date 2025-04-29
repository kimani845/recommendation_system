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
    return redirect(url_for('record_sales'))

@app.route('/record_sales', methods=['GET', 'POST'])
def record_sales():
    if request.method == 'POST':
        date = request.form['date']
        region = request.form['region']
        sales_data = {}
        try: 
            for cakes in CAKE_TYPES:
                sales_data[cakes] = int(request.form[cakes])
        except ValueError:
            flash("Invalid sales data. Please enter valid numbers.")
            return redirect(url_for('record_sales'))
        
        tracker.add_daily_sales(date, region, sales_data)
        flash("Sales data recorded successfully!")
        return redirect(url_for('record_sales'))
    
    return render_template('record_sales.html', cake_types=CAKE_TYPES, regions=REGIONS)

@app.route('/generate_predictions', methods=['GET', 'POST'])