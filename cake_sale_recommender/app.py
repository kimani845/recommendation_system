# Flask Main App
from flask import Flask, render_template, request, redirect, url_for, flash
from cake_sales_analysis import CakeSalesTracker
from recommender import generate_recommendations
from database import get_connection, get_all_cake_types, get_all_regions
from datetime import datetime 
from database import initialize_database

# Initialize database tables on first run
initialize_database()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
tracker = CakeSalesTracker()

@app.route('/')
def index():
    return redirect(url_for('analysis'))
@app.route('/record_sales', methods=['GET', 'POST'])
def record_sales():
    # Fetch cake types and regions from the database
    cake_types = [ct[0] for ct in get_all_cake_types()]
    regions = [r[0] for r in get_all_regions()]
    
    if request.method == 'POST':
        date = request.form['date']
        region = request.form['region']
        
        # Ensure region is valid
        if region not in regions:
            flash("Invalid region selected.")
            return redirect(url_for('record_sales'))

        sales_data = {}
        try: 
            for cake in cake_types:
                sales_data[cake] = int(request.form.get(cake, 0))
        except ValueError:
            flash("Invalid sales data. Please enter valid numbers.")
            return redirect(url_for('record_sales'))
        
        # Add the sales data (ensure date format is correct)
        try:
            tracker.add_daily_sales(datetime.strptime(date, '%Y-%m-%d'), region, sales_data)
            flash("Sales data recorded successfully!")
        except Exception as e:
            flash(f"Error recording sales data: {str(e)}")
        
        return redirect(url_for('record_sales'))
    
    return render_template('record_sales.html', cake_types=cake_types, regions=regions)


@app.route('/generate_predictions', methods=['GET', 'POST'])
def generate_predictions():
    predictions = {}
    cake_types = [ct[0] for ct in get_all_cake_types()]
    regions = [r[0] for r in get_all_regions()]
    
    if request.method == 'POST':
        date = request.form['date']
        region = request.form['region']
        try: 
            predictions = tracker.predict_next_day(datetime.strptime(date, '-%Y-%m-%d'), region)
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.")
            return redirect(url_for('generate_predictions'))
        predictions = tracker.predict_next_day(date, region)
        if predictions:
            tracker.add_prediction_to_excel(datetime.strptime(date, '-%Y-%m-%d'), region, predictions)
            flash("Prediction generated successfully!")
        else:
            flash("Failed to generate prediction. Please train the model first.")
    return render_template('generate_predictions.html', cake_types=cake_types, regions=regions, predictions=predictions)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    cake_types = [ct[0] for ct in get_all_cake_types()]
    regions = [r[0] for r in get_all_regions()]
    recommendations = {}

    if request.method == 'POST':
        region = request.form['region']
        try:
            recommendations = generate_recommendations(region=region)
        except Exception as e:
            flash(f"Error generating recommendations: {e}")

    return render_template('recommendations.html', cake_types=cake_types, regions=regions, recommendations=recommendations)

@app.route('/analysis')
def analysis():
    try: 
        tracker.update_summaries()
        tracker.update_dashboard()
    except Exception as e:
        flash(f"Error updating analysis: {e}")
        return redirect(url_for('analysis'))
    return render_template('analysis.html')

@app.route('/train-model')
def train_model():
    try:
        tracker.train_prediction_model()
        flash("Model trained successfully!", "info")
    except Exception as e:
        flash(f"Error training model: {e}")
    return redirect(url_for('base'))

@app.route('/download-report')
def download_report():
    return send_file(tracker.excel_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)