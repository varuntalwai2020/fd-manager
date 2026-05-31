# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from .reminder import check_fd_maturity

def start():
    print("=== SCHEDULER STARTED ===")

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_fd_maturity, 'interval', minutes=1)
    scheduler.start()
