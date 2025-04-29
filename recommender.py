from datetime import datetime, timedelta
from database  import get_connection

def get_recent_sales(region=None, days=30):
    """Get recent sales data for a specific region or all regions"""
    conn=get_connection()
    conn=conn.cursor()
    
    since_date = (datetime.now() - timedelta(days=days).date)
    
    if region:
        cursor.execute(
            '''
            SELECT ct.name, SUM(s.quantity)
            FROM sales s 
            JOIN cake_types ct ON s.cake_id = ct.id
            JOIN regions r ON s.region_id = r.id
            WHERE r.name = ? AND s.sale_date >= ?
            GROUP BY ct.name
            ORDER BY SUM (s.quantity) DESC
            ''',
                (region, since_date)

        )
    else:
        cursor.execute(
            '''
            SELECT ct.name, SUM(s.quantity)
            FROM sales s 
            JOIN cake_types ct ON s.cake_id = ct.id
            JOIN regions r ON s.region_id = r.id
            WHERE s.sale_date >= ?
            GROUP BY ct.name
            ORDER BY SUM (s.quantity) DESC
            ''',
                (since_date,)

        )