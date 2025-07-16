# 📋 Naman TaskBoard

A full-featured FastAPI task management app with:

- 🔐 Login/logout (session-based)
- 📝 Add/Edit/Delete tasks
- ⚙️ Task generator with `/generate`
- 🔁 Recurring daily task generation (APScheduler)
- 📊 Dashboard with Chart.js (`/dashboard`)
- 🔍 Search & filter tasks
- ⬇️ Export to CSV (`/export`)
- 🕒 Auto logout after 10 minutes of inactivity

## 🌐 Live App
**URL:** [https://naman9.onrender.com](https://naman9.onrender.com)

## 👨‍💻 Login Credentials
| Username | Password |
|----------|----------|
| `admin`  | `123`    |
| `naman`  | `123`    |

## 🚀 Deployment
This app is deployed on **Render.com** and automatically runs with:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
