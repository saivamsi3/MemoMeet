# Deployment Guide

## Local Development
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env` and set your GEMINI_API_KEY
4. `python app.py`

## Render Deployment
1. Push to GitHub
2. Connect repo to Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Add environment variables

## Railway Deployment
1. Connect GitHub repo to Railway
2. It auto-detects Python
3. Set `GEMINI_API_KEY` in variables

## PythonAnywhere
1. Upload files
2. Create virtualenv
3. Configure WSGI file
4. Set environment variables
