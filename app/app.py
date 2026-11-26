import os
import git
import secrets
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlencode
import hashlib
import hmac
from fastapi import HTTPException

from flask import Flask, render_template, send_from_directory
from flask import redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

from pizza_chart.heatmap import create_heatmap_figure

def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.
    Raise and return 403 if not authorized.
    From: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries#python-example

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")

# Define useful paths
ROOT_DIR = Path(__file__).parent.parent.resolve() # get the absolute path of the directory root
APP_DIR = ROOT_DIR / "app"
DATA_DIR = ROOT_DIR / "data"

# Load environment variables from .env file
load_dotenv(ROOT_DIR / ".env") # needed for local development, but not in production where environment variables are set from /var/www/pizzachart_pythonanywhere_com_wsgi.py

# Load the app
app = Flask(__name__, static_folder=ROOT_DIR / "static")

# Load the secrets from environment variables
app.secret_key = os.environ["FLASK_SECRET_KEY"]

GITHUB_CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
GITHUB_CLIENT_SECRET = os.environ["GITHUB_CLIENT_SECRET"]

# Configure the database
os.makedirs(DATA_DIR, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{DATA_DIR}/data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class TestEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)

# Application home page
@app.route("/")
def index():
    heatmap_html = create_heatmap_figure(DATA_DIR / "data.csv").to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={"displayModeBar": False, "responsive": True},
    )
    return render_template(
        "index.html",
        username=session.get("github_username"),
        heatmap_html=heatmap_html,
    )


@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(ROOT_DIR / "assets", filename)

# Login page
@app.route("/auth/login")
def github_login():
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": url_for(
            "github_callback",
            _external=True
        ),
        "scope": "read:user",
        "state": state,
    }

    return redirect(
        "https://github.com/login/oauth/authorize?"
        + urlencode(params)
    )

# Redirect page when a user logs in
@app.route("/auth/callback")
def github_callback():
    # Verify OAuth state
    state = request.args.get("state")
    expected_state = session.pop("oauth_state", None)

    if not expected_state or state != expected_state:
        return "Invalid OAuth state", 400

    # Handle authorization denial
    if request.args.get("error"):
        return "GitHub authorization denied", 403

    code = request.args.get("code")
    if not code:
        return "Missing authorization code", 400

    # Exchange authorization code for access token
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
        timeout=10,
    )

    response.raise_for_status()
    token_data = response.json()

    access_token = token_data.get("access_token")
    if not access_token:
        return "Could not obtain GitHub access token", 400

    # Retrieve authenticated user's GitHub identity
    user_response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )

    user_response.raise_for_status()
    github_user = user_response.json()

    # Store identity in Flask session
    session["github_username"] = github_user["login"]

    return redirect("/") # redirect to home page


# Logout page
@app.route("/auth/logout")
def github_logout():
    # Logout from GitHub by clearing the session
    session.clear()
    return redirect("/") # redirect to home page

# Pull from GitHub on webhook
@app.route('/gh_webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Verify the webhook signature
        verify_signature(request.data, os.environ["WEBHOOK_SECRET"], request.headers.get("X-Hub-Signature-256"))
        # Pull the latest changes from GitHub
        repo = git.Repo('/home/pizzachart/pizza_chart')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400