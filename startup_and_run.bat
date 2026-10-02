@echo off
setlocal
cd /d %~dp0

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate

echo.
echo Starting Pet Adoption and Rescue Platform...
echo Open http://127.0.0.1:8000/
echo.
python manage.py runserver
endlocal
