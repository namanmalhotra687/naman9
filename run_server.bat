@echo off
cd /d %~dp0
echo Starting FastAPI app...
python -m uvicorn main:app --reload --port 10000
pause
