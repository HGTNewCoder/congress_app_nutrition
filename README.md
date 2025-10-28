# LiveHealthy — Local Development

A minimal Flask app for looking up local health and nutrition information. The project uses plain HTML templates, static assets (CSS/JS), and a small Flask server located in `app.py`.

## Prerequisites
- Python 3.8+ (3.10+ recommended)
- Google Cloud project + API key and service account JSON (required for features that call Google Cloud services)

## Quick start (Windows PowerShell)

Open PowerShell and run:

```powershell
# create a virtual environment
python -m venv .venv

# activate the venv (PowerShell)
. .venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt

# run the app
python app.py
```

Open http://127.0.0.1:10000 in your browser.

If PowerShell blocks script execution when activating the venv, you can temporarily allow local scripts in your user scope:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Environment configuration

This project expects a `key.json` service account file and a `.env` (or environment variables) for Google Cloud values if you want to use Google APIs. Create a `.env` file in the project root with the following variables (example):

```env
MODEL=
PROJECT=
LOCATION=
GOOGLE_APPLICATION_CREDENTIALS=key.json
GOOGLE_API_KEY=
```

Notes:
- `GOOGLE_APPLICATION_CREDENTIALS` should point to the service account JSON file (e.g., `key.json`).
- `GOOGLE_API_KEY` is required for simple API key access to some Google services.
- If you don't need Google Cloud features for local testing, you can omit these files — the app will still run, but some functionality may be disabled or return errors.

## Project structure

- `app.py` — Flask application entrypoint
- `templates/` — HTML templates (home, ask, map, about, etc.)
- `static/` — CSS, JS, and images
- `requirements.txt` — Python dependencies
- `key.json` — (not committed) Google service account credentials — add to `.gitignore`

## Useful routes

Depending on the app configuration, the following routes are typically available:

- `/` — Home page
- `/ask` — Ask page (user can submit questions)
- `/map` — Map view
- `/hospitals_near_me` — Hospitals nearby (static or dynamic view)
- `/about` — About page

Open the templates in `templates/` to see exact route names if any custom routes are used in `app.py`.

## Troubleshooting

- If requirements fail to install, ensure your pip is up to date: `python -m pip install --upgrade pip`.
- If Google Cloud calls fail, verify: the `key.json` path, `GOOGLE_APPLICATION_CREDENTIALS`, and that the service account has the proper IAM roles for the APIs used.
- If the app runs but pages show errors, check the console/log output from the terminal where `python app.py` is running.
---
