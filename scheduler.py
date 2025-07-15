from apscheduler.schedulers.background import BackgroundScheduler
from generator_logic import generate_task
from model import SessionLocal
from controller import add_item, update_item

def run_daily_task():
    db = SessionLocal()
    try:
        task = generate_task("Daily")
        add_item(task['title'], task['description'], task['username'], db)
        latest_id = db.query(update_item.__annotations__['item_id']).order_by(-1).first().id
        update_item(latest_id, task['title'], task['description'], task['username'], task['status'], task['deadline'], db)
        print("✅ Daily task generated.")
    except Exception as e:
        print("❌ Scheduler Error:", e)
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_daily_task, "interval", days=1)  # Change to hours=1 or seconds=30 for testing
    scheduler.start()
