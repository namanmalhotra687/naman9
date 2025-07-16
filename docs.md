# 📘 Naman TaskBoard – Developer Docs

## 🔐 Auth

- `/login` (GET): Show login form
- `/login` (POST): Authenticate user
- `/logout`: Clear session and redirect to login

## 🏠 Task Routes

| Route             | Method | Description              |
|------------------|--------|--------------------------|
| `/home`          | GET    | Show tasks (after login) |
| `/add`           | POST   | Add new task (Form)      |
| `/edit/{id}`     | POST   | Edit task (Form)         |
| `/delete/{id}`   | GET    | Delete a task            |
| `/items`         | GET    | Get all tasks (JSON)     |
| `/add-json`      | POST   | Add task via JSON        |
| `/edit-json/{id}`| PUT    | Edit task via JSON       |

## ⚙️ Generate & Recurrence

- `/generate` (GET): Show generate form
- `/generate` (POST): Add random task
- APScheduler: Auto-generate daily tasks

## 📊 Dashboard

- `/dashboard`: Pie chart of task status

## ⬇️ Export

- `/export`: Export all tasks as `.csv`

## 💡 Notes

- Auto logout after 10 mins of inactivity (JS)
- Task filtering/search supported via query params
