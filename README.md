# Cake Sales Tracker and Recommendation System

This system helps you track your cake sales, analyze trends, and predict future sales to optimize your ordering process.

## Features

- **Daily Sales Tracking**: Record sales of different cake types by region
- **Sales Analysis**: Analyze sales by day of week, region, and cake type
- **Prediction System**: Machine learning model to predict future sales
- **Dashboard**: Visual representation of sales data
- **User Interface**: Easy-to-use interface for data entry and analysis

## Cake Types Tracked

- Heart Cakes
- Coconut Cakes
- Mobile Cakes
- Block Cakes
- Star Cakes
- Queen Cakes
- Sweet Cakes

## Getting Started

### Prerequisites

To run this system, you need:

- Python 3.7 or higher
- Required Python packages:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scikit-learn
  - openpyxl
  - tkinter
  - tkcalendar

### Installation

1. Install the required packages:

```
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl tkcalendar
```

2. Run the user interface:

```
python cake_sales_ui.py
```

## How to Use

### Recording Sales

1. Go to the "Record Sales" tab
2. Select the date and region
3. Enter the number of each cake type sold
4. Click "Record Sales"

### Generating Predictions

1. Go to the "Predictions" tab
2. Select the date and region for prediction
3. Click "Train Model" (if you haven't already)
4. Click "Generate Prediction"

### Analyzing Sales

1. Go to the "Analysis" tab
2. Click "Update Summaries" to refresh the analysis
3. Click "Update Dashboard" to update the visual dashboard
4. Click "Open Excel File" to view the full Excel workbook

## Excel Workbook Structure

The system creates an Excel workbook with the following sheets:

- **Daily Sales**: Raw sales data by date, region, and cake type
- **Weekly Summary**: Sales aggregated by week
- **Monthly Analysis**: Sales aggregated by month
- **Day of Week Analysis**: Sales patterns by day of week
- **Regional Analysis**: Sales patterns by region
- **Predictions**: Predicted sales for future dates
- **Dashboard**: Visual representation of key metrics

## Recommendation Algorithm

The system uses a Random Forest Regressor model to predict sales based on:

- Day of the week
- Month
- Day of the month
- Region

The model is trained on your historical sales data and learns patterns such as:
- Which cakes sell better on specific days
- Regional preferences for different cake types
- Seasonal variations in sales

## Best Practices

1. **Record sales daily**: The more data you have, the better the predictions will be
2. **Retrain the model regularly**: As you add more sales data, retrain the model to improve predictions
3. **Use predictions as a guide**: The system provides recommendations, but use your judgment for final decisions
4. **Analyze trends**: Regularly check the analysis to understand changing customer preferences

## Customization

You can customize the system by editing the Python files:

- To add or change cake types, modify the `CAKE_TYPES` list in `cake_sales_analysis.py`
- To add or change regions, modify the `REGIONS` list in `cake_sales_analysis.py`
- To customize the user interface, modify `cake_sales_ui.py`