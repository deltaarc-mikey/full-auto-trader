# scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from scanner_task import run_scanner_task
import datetime

scheduler = BlockingScheduler(timezone="America/New_York")

# Schedule the backend scanner task to run at your desired times
print("Scheduler configured to run analysis at set times...")

# Run pre-market job: 8:45 AM ET every weekday
scheduler.add_job(run_scanner_task, 'cron', day_of_week='mon-fri', hour=8, minute=45)

# Run market-hour check: 12:00 PM ET every weekday
scheduler.add_job(run_scanner_task, 'cron', day_of_week='mon-fri', hour=12, minute=0)

# Run end-of-day review: 3:45 PM ET every weekday
scheduler.add_job(run_scanner_task, 'cron', day_of_week='mon-fri', hour=15, minute=45)

# Start the scheduler
print("Scheduler started... This terminal will run background jobs. Press Ctrl+C to exit.")
scheduler.start()