# LiveHealthy — Local Development

This is a minimal Flask web app (Home, Ask, Something, About pages). The project uses plain HTML templates, CSS, and a small JavaScript file for the sidebar.

Requirements
- Python 3.10+ (3.8+ should work)

Set up and run (Windows PowerShell)

```powershell
# create and activate a venv
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt

# run the app
$env:FLASK_APP = 'app.py'; $env:FLASK_ENV = 'development'; python .\app.py
```

Notes
- Drop a `logo.png` image into `static/` to show your PNG logo in the top-left. If no image is present the logo container will fall back to the gradient background.
- `templates/about.html` is pre-filled with example content you can edit.
- If you want me to add a simple Ask form that saves to CSV, say so and I'll wire it up.
