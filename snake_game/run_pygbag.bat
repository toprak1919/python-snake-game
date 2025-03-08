@echo off
echo Starting Pygbag web server...
echo.
echo When the server starts, open your browser and go to:
echo http://localhost:8000
echo.
python -m pygbag --port 8000 .
pause
