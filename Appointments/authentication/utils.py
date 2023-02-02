from django.utils import timezone
from datetime import datetime
from django.utils.formats import localize

def get_current_start_end_time():
    start_date = timezone.now().strftime("%Y-%m-%d")
    date_start = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
    date_end = date_start+ timezone.timedelta(days=1)
    return {"date_start":date_start, "date_end":date_end}