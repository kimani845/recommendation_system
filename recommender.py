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
    recent_sales = cursor.fetchall()
    conn.close()
    return recent_sales


def generate_recommendations(region=None, days=30, top_n=3):
    """Generate recommendations based on recent sales data"""
    recent_sales = get_recent_sales(region, days)
    recommendations = [cake for cake, _ in recent_sales[:top_n]]
    return recommendations