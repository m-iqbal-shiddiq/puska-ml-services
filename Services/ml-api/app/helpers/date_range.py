from datetime import timedelta

def create_date_range(start_date, end_date):
    result_date = []
    
    current_date = start_date
    while current_date <= end_date:
        result_date.append([
            current_date.year,
            current_date.month,
            current_date.day
        ])
        
        current_date += timedelta(days=1)
        
    return result_date