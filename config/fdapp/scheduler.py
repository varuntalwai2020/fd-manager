from apscheduler.schedulers.background import BackgroundScheduler
from .reminder import check_fd_maturity

scheduler = BackgroundScheduler()

def start():

    if scheduler.running:
        return

    scheduler.add_job(
        check_fd_maturity,
        'interval',
        minutes=1,
        id='check_fd_maturity',
        replace_existing=True,
        max_instances=1,
        coalesce=True
    )

    scheduler.start()

    print("=== SCHEDULER STARTED ===")
