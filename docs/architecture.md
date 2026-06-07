# MemoMeet Architecture

## Overview
MemoMeet is a Flask-based web application with AI-powered meeting intelligence.

## Tech Stack
- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite
- **Frontend:** Bootstrap 5, Chart.js
- **AI:** Google Gemini API
- **PDF:** ReportLab

## Structure
- `app.py` - Application factory
- `models/` - SQLAlchemy models
- `routes/` - Blueprint route handlers
- `services/` - Business logic layer
- `ai/` - Gemini AI integration
- `utils/` - Helper utilities
- `templates/` - Jinja2 templates
- `static/` - CSS, JS, assets
