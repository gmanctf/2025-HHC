# app/main.py
import requests
import logging
from flask import Flask, request, Response, jsonify, render_template, redirect, url_for, session, flash, render_template_string
from functools import wraps
import os
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
#app.secret_key = os.urandom(32)  # Generates a secure 32-byte random key
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'secure_sites_dont_get_leaked_right')  # Use an environment variable or a default value
secret_password = os.getenv('SECRET_PASSWORD', 'an_elf_and_password_on_a_bird')  # Use an environment variable or a default value
# Change this to the URL of your LLM API
LLM_API_URL = os.getenv('CHATBOT_URL', 'http://localhost:5000')

USERS = {
    "admin": secret_password  # The LLM password to be leaked
}
USERS_PHOTO = {
    "admin": ""
}


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def stream_response(user_prompt):
    response = requests.post(LLM_API_URL+"/api/chat", json={"prompt": user_prompt}, stream=True)
    
    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk.decode()
    
    return Response(generate(), content_type='text/plain')

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    username = session.get('username')
    photo = USERS_PHOTO.get(username)
    if photo == "":
        photo = url_for('static', filename='images/default.jpg')
    logger.info(f"[*] Photo: {photo}")
    return render_template('profile.html',photo=photo)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    logger.info(f"[*] Contents of multipart form: {request.files}")
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('profile'))
    username = session.get('username')
    logger.info(f"[*] Username: {username}")
    logger.info(f"[*] Request files: {request.files}")
    new_photo = request.files['file']
    logger.info(f"[*] New photo: {new_photo.filename}")

    if new_photo:
        try:
            # Ensure directory exists
            os.makedirs('static/images', exist_ok=True)
            logger.info(f"[+] Path: {os.path.join('static/images', new_photo.filename)}")
            # Create a safe filename
            safe_filename = f"{username}_{os.urandom(8).hex()}.png"
            logger.info(f"[+] Safe filename: {safe_filename}")
            filepath = os.path.join('static/images', safe_filename)
            logger.info(f"[+] Filepath: {filepath}")
            # Save the photo content
            new_photo.save(filepath)
            logger.info(f"[+] Saving profile picture for {username}")
            # Update the photo path in the user's profile
            USERS_PHOTO[username] = f"/static/images/{safe_filename}"
            logger.info(f"[*] USERS_PHOTO: {USERS_PHOTO}")
        except Exception as e:
            flash(f'Error saving profile picture: {str(e)}', 'error')
            return redirect(url_for('profile'))
    # Save the temporary photo path to the user's profile
    return redirect(url_for('dashboard')+"?username="+username)

@app.route('/dashboard')
@login_required
def dashboard():
    # Directly render the username as a template expression
    temp_username = request.args.get('username')
    username_template = f"{session['username']}"
    logger.info(f"[*] Temp username: {temp_username}")
    if temp_username is None:
        temp_username = username_template
    dangerous_patterns = re.compile(r'<|>|self|config|class|mro|x|_|\.')
    if dangerous_patterns.search(temp_username):
        logger.info(f"[!] Dangerous pattern detected {dangerous_patterns.search(temp_username)}")
        for i in dangerous_patterns.findall(temp_username):
            temp_username = temp_username.replace(i, '')
        logger.info(f"[!] Dangerous pattern removed {temp_username}")
    
    
    username_rendered = render_template_string(temp_username)
    
    # Then include the rendered result in the template
    template = '''
    {% extends "base.html" %}
    {% block title %}Frosty Frostafier Dashboard{% endblock %}
    {% block content %}
        <div class="container">
            <h1>Frosty Frostafier Dashboard</h1>
            <p class="welcome-message">Welcome back, <span class="username-sparkle">{{ username_rendered|safe }}</span>! ❄</p>
            
            <div class="festive-dashboard">
                <div class="dashboard-card">
                    <h3>🤖 Gnome bot status</h3>
                    <div class="progress">
                        <div class="progress-bar bg-success" role="progressbar" style="width: 95%" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100">67%</div>
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <h3>❄ Weather in the Neighborhood</h3>
                    <p>Current temperature: Not cold enough!</p>
                    <p>Target temperature: Frosty</p>
                </div>
                
                <div class="dashboard-card">
                    <h3>🎁 Motivational Quote</h3>
                    <p>Being cold is a state of mind!</p>
                </div>
            </div>
            
            <div class="dashboard-message">
                <p><em>The plan is working!</em></p>
            </div>
        </div>
    {% endblock %}
    '''
    return render_template_string(template, username_rendered=username_rendered)

@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    if new_password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('profile'))
    else:
        username = session.get('username')
        logger.info(f"[*] Updating USERS[{username}]")
        USERS[username] = new_password
        logger.info(f"[*] New password for USERS[{username}]: {USERS[username]}")

        flash('Password updated successfully')
        return redirect(url_for('dashboard')+"?username="+username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_url = request.args.get('next', url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('You were successfully logged in')
            return redirect(next_url)
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/ask', methods=['POST'])
def ask(): # Create a middleman docker compose container to forward to chatbot requests, needs api key to be accessed
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' field"}), 400
    
    return stream_response(data['prompt'])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8080), debug=False)
