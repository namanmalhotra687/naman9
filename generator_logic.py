import random
from datetime import datetime, timedelta

def generate_task(local_kw: str = ""):
    titles = [
        "Fix login bug", "Design landing page", "Optimize database",
        "Implement user auth", "Write unit tests", "Deploy to Render"
    ]
    descriptions = [
        "Urgent", "Low priority", "Requires review", "Client feedback", "Add documentation"
    ]
    status_options = ["New", "In Progress", "Done"]

    return {
        "title": f"{local_kw} {random.choice(titles)}".strip(),
        "description": random.choice(descriptions),
        "username": "generator",
        "status": random.choice(status_options),
        "deadline": (datetime.now() + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d')
    }
