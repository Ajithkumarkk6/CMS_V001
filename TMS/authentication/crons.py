
from django.utils import timezone
from datetime import datetime


def my_cron_job():
    print("cron called")
    print("cron called3==========")
    print(timezone.now())
    print("cron called3==========")
    # your functionality goes here
