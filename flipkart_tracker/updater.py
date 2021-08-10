from .views import items_update
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(items_update,'interval', minutes=5)
    scheduler.start()
