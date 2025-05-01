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
                sales_data[cakes] = int(request.form.get(cakes, 0))
        except ValueError:
            flash("Invalid sales data. Please enter valid numbers.")
            return redirect(url_for('record_sales'))
        
        tracker.add_daily_sales(datetime.strptime(date, '-%Y-%m-%d'), region, sales_data)
        flash("Sales data recorded successfully!")
        return redirect(url_for('record_sales'))
    
    return render_template('record_sales.html', cake_types=CAKE_TYPES, regions=REGIONS)

@app.route('/generate_predictions', methods=['GET', 'POST'])
def generate_predictions():
    predictions = {}
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
    return render_template('generate_predictions.html', cake_types=CAKE_TYPES, regions=REGIONS, predictions=predictions)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    recommendations = {}
    if request.method == 'POST':
        region = request.form['region']
        recommendations = generate_recommendations(region=region)
    return render_template('recommendations.html', cake_types=CAKE_TYPES, regions=REGIONS, recommendations=recommendations)


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