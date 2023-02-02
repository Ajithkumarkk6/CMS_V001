from django.utils import timezone
from datetime import datetime, tzinfo

def get_start_end_date_today():

    start_date = timezone.now()
    end_date = timezone.now() + timezone.timedelta(days=1)

    tzinfoccode = timezone.get_current_timezone() 
    # date_start = start_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzinfoccode)
    # date_end = end_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzinfoccode)
    date_start = start_date
    # .replace(tzinfo=tzinfoccode) 
    # + timezone.timedelta(hours=5, minutes=30)
    # date_start = date_start.replace(hour=0, minute=0, second=0, microsecond=0) 
    # + timezone.timedelta(hours=5, minutes=30)
    date_end = end_date
    # .replace(tzinfo=tzinfoccode) 
    # + timezone.timedelta(hours=5, minutes=30)
    # end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(hours=5, minutes=30)

    # print(timezone.is_aware(date_start))
    
    # print(tzinfoccode)
    # ====================================
    
    # now = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
    # print now.astimezone(timezone.utc)
    
    # date_start = timezone.utc()
    date_start = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
    date_start =date_start.replace(hour=5, minute=30, second=0, microsecond=0)
    date_end = date_start + timezone.timedelta(days=1)
    response = {'date_start': date_start, 'date_end':date_end}
    print("ddddddddddddddddddddddddddddddddddddddddd")
    print(response)

    return response

def get_start_end_date_month():

    start_date = timezone.now()
    end_date = timezone.now() + timezone.timedelta(days=1)

    tzinfoccode = timezone.get_current_timezone() 

    date_start = start_date
    date_end = end_date

    date_start = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
    date_start = date_start.replace(hour=5, minute=30, second=0, microsecond=0)
    date_end = date_start + timezone.timedelta(days=1)
    date_start = date_start.replace(day=1)
    
    response = {'date_start': date_start, 'date_end':date_end}

    return response

# def get_start_end_date_today2():
#     start_date = timezone.now() + timezone.timedelta(days=-1)
#     # .strftime("%Y-%m-%d")
#     end_date_tz = start_date + timezone.timedelta(days=1) 
#     end_date = end_date_tz
#     # .strftime("%Y-%m-%d")


#     tzinfoccode = timezone.get_current_timezone() 
    
#     print(tzinfoccode)
#     # date_start = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
#     # date_end = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
#     # .astimezone(current_tz)
#     # (datetime.strptime(start_date, '%Y-%m-%d'))

#     date_start = start_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzinfoccode)
#     date_end = end_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tzinfoccode)
    
#     # date_start = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
#     # date_end = end_date.replace(hour=0, minute=0, second=0, microsecond=0)


#     response = {}
#     response['date_start'] = date_start
#     response['date_end'] = date_end
#     print("ddddddddddddddddddddddddddddddddddddddddd")
#     print(response)
#     return response

def get_start_end_date_per_month_from_request(date):
    date_start = get_zone_aware_date_from_request(date) 
    date_start =date_start.replace(hour=5, minute=30, second=0, microsecond=0)
    date_end = date_start + timezone.timedelta(days=1)
    date_end =date_end.replace(hour=5, minute=30, second=0, microsecond=0)

    date_start = date_start.replace(day=1)
    response = {'date_start': date_start, 'date_end':date_end}
    return response


def get_start_end_date_from_request(date):
    date_start = get_zone_aware_date_from_request(date) 
    # date_start =date_start.replace(hour=5, minute=30, second=0, microsecond=0)
    date_end = date_start + timezone.timedelta(days=1)
    # date_end =date_end.replace(hour=5, minute=30, second=0, microsecond=0)
    response = {'date_start': date_start, 'date_end':date_end}
    return response

def get_zone_aware_date_from_request(date):
    date = timezone.make_aware(datetime.strptime(date, '%Y-%m-%d'))
    return date

def get_current_time_aware():
    start_date = timezone.now()
    return start_date
  
def add_day(date_received, nums):
    return date_received + timezone.timedelta(days=nums)
  
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)