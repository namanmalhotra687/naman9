import os
import psutil

db_path = "test.db"

# Step 1: Find and kill processes locking the file
for proc in psutil.process_iter(['pid', 'name', 'open_files']):
    try:
        for f in proc.info['open_files'] or []:
            if f.path.endswith(db_path):
                print(f"❌ Locking process found: {proc.info['name']} (PID {proc.info['pid']})")
                proc.terminate()
                proc.wait(timeout=5)
                print("✅ Process terminated.")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# Step 2: Delete the file
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("✅ Deleted test.db successfully.")
    except Exception as e:
        print(f"⚠️ Could not delete: {e}")
else:
    print("ℹ️ test.db does not exist.")
