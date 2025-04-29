from datetime import datetime, timedelta
from database  import get_connection

def get_recent_sales(region=None, days=30):
    """Get recent sales data for a specific region or all regions"""
    conn=get_connection()
    conn=conn.cursor()