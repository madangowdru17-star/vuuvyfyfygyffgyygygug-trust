# main.py
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from flask_cors import CORS
import json
import os
import hashlib
import secrets
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

CONFIG_FILE = 'config.json'
ADMIN_CREDENTIALS_FILE = 'admin_credentials.json'

DEFAULT_CONFIG = {
    "maintenance": False,
    "freefire_maintenance": False,
    "freefire_max_maintenance": False,
    "master_key": "HEXPROXY999",
    "master_key_expiry": "2026-12-31T23:59:59.000000",
    "login_name": "HEX PROXY XOS V6",
    "app_name": "HEX PROXY XOS V6",
    "maintenance_message": "We are performing scheduled maintenance. Please join our Telegram for updates.",
    "telegram_link": "https://t.me/+_s4OBzblpi0zNzE1",
    "get_key_link": "https://t.me/+_s4OBzblpi0zNzE1",
    "logo_url": "https://i.ibb.co/Wpcb6Ydy/IMG-20260313-030403-360.jpg",
    "shizuku_logo_url": "https://i.ibb.co/JRjy2ZpC/20260808-044938.png",
    "freefire_logo_url": "https://i.ibb.co/nsqT2bjJ/Garena-Free-Fire-Icon.jpg",
    "freefire_max_logo_url": "https://i.ibb.co/Wv5pthbL/unnamed.webp",
    "api_base_url": "https://key-system-production-1bc5.up.railway.app",
    "update_available": False,
    "update_version": "2.1.0",
    "update_changelog": "- Fixed AimBot\n- Added new features\n- Performance improvements",
    "update_url": "https://github.com/madangowdru17-star/Apk/raw/refs/heads/main/generated_sign.apk",
    "assets_version": "9.9",
    "assets": [
        {
            "name": "bg.mp4",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/bg.mp4"
        }
    ],
    "freefire_buttons": [
        {
            "id": "ff_drag",
            "name": "Chest HS 95%-Sensi",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "ff_antenna",
            "name": "DRAG HS + ANITENA SPEED 2x",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/DARG-HS-1000/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": True
        },
        {
            "id": "ff_headshot",
            "name": "HEADSHOT 99%",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        },
        {
            "id": "ff_aimbot",
            "name": "AIMBOT PRO",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        },
        {
            "id": "ff_wallhack",
            "name": "WALLHACK XRAY",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        },
        {
            "id": "ff_esp",
            "name": "ESP PLAYER",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        }
    ],
    "freefire_max_buttons": [
        {
            "id": "max_drag_safe",
            "name": "DRAG HS 85% SAFE",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/HS-ANTENA/refs/heads/main/localconfig.json",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_nick",
            "name": "NICK HS 95%",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_body",
            "name": "BODY HS 99%",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_aimbot",
            "name": "AIMBOT MAX",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_wallhack",
            "name": "WALLHACK MAX",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_esp",
            "name": "ESP MAX",
            "url": "",
            "enabled": True,
            "maintenance": False
        }
    ],
    "root_libs": [
        {
            "id": "root_max64",
            "name": "FF MAX 64-BIT",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libcrashlytics_arm64.so",
            "lib_path": "lib/arm64-v8a/libcrashlytics.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_max32",
            "name": "FF MAX 32-BIT",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libcrashlytics_arm.so",
            "lib_path": "lib/armeabi-v7a/libcrashlytics.so",
            "arch": "arm",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_aimbot",
            "name": "AIMBOT MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libaimbot.so",
            "lib_path": "lib/arm64-v8a/libaimbot.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_esp",
            "name": "ESP MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libesp.so",
            "lib_path": "lib/arm64-v8a/libesp.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_headshot",
            "name": "HEADSHOT MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libheadshot.so",
            "lib_path": "lib/arm64-v8a/libheadshot.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_wallhack",
            "name": "WALLHACK MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libwallhack.so",
            "lib_path": "lib/arm64-v8a/libwallhack.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        }
    ]
}

def load_admin_credentials():
    if os.path.exists(ADMIN_CREDENTIALS_FILE):
        try:
            with open(ADMIN_CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"admins": []}
    return {"admins": []}

def save_admin_credentials(credentials):
    with open(ADMIN_CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin(username, password):
    credentials = load_admin_credentials()
    for admin in credentials['admins']:
        if admin['username'] == username:
            return True
    hashed_pw = hash_password(password)
    credentials['admins'].append({
        'username': username,
        'password': hashed_pw,
        'created_at': datetime.now().isoformat()
    })
    save_admin_credentials(credentials)
    return True

def verify_admin(username, password):
    credentials = load_admin_credentials()
    hashed_pw = hash_password(password)
    for admin in credentials['admins']:
        if admin['username'] == username and admin['password'] == hashed_pw:
            return True
    return False

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# =============== API ROUTES ===============

@app.route('/api/config', methods=['GET'])
def get_config():
    config = load_config()
    return jsonify(config)

@app.route('/api/button/toggle/<button_type>/<button_id>', methods=['POST'])
@login_required
def toggle_button(button_type, button_id):
    try:
        data = request.json
        enabled = data.get('enabled', False)
        maintenance = data.get('maintenance', False)
        
        config = load_config()
        
        if button_type == 'freefire':
            buttons = config.get('freefire_buttons', [])
        elif button_type == 'freefire_max':
            buttons = config.get('freefire_max_buttons', [])
        elif button_type == 'root_libs':
            buttons = config.get('root_libs', [])
        else:
            return jsonify({"success": False, "message": "Invalid button type"}), 400
        
        for button in buttons:
            if button.get('id') == button_id:
                button['enabled'] = enabled
                button['maintenance'] = maintenance
                
                if button_type == 'freefire':
                    config['freefire_buttons'] = buttons
                elif button_type == 'freefire_max':
                    config['freefire_max_buttons'] = buttons
                elif button_type == 'root_libs':
                    config['root_libs'] = buttons
                
                save_config(config)
                return jsonify({"success": True, "message": "Button toggled successfully", "enabled": enabled, "maintenance": maintenance})
        
        return jsonify({"success": False, "message": "Button not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/button/update/<button_type>/<button_id>', methods=['POST'])
@login_required
def update_button(button_type, button_id):
    try:
        data = request.json
        config = load_config()
        
        if button_type == 'freefire':
            buttons = config.get('freefire_buttons', [])
        elif button_type == 'freefire_max':
            buttons = config.get('freefire_max_buttons', [])
        elif button_type == 'root_libs':
            buttons = config.get('root_libs', [])
        else:
            return jsonify({"success": False, "message": "Invalid button type"}), 400
        
        for button in buttons:
            if button.get('id') == button_id:
                if 'url' in data:
                    button['url'] = data['url']
                if 'name' in data:
                    button['name'] = data['name']
                
                if button_type == 'freefire':
                    config['freefire_buttons'] = buttons
                elif button_type == 'freefire_max':
                    config['freefire_max_buttons'] = buttons
                elif button_type == 'root_libs':
                    config['root_libs'] = buttons
                
                save_config(config)
                return jsonify({"success": True, "message": "Button updated successfully"})
        
        return jsonify({"success": False, "message": "Button not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/maintenance/toggle', methods=['POST'])
@login_required
def toggle_maintenance():
    try:
        data = request.json
        config = load_config()
        
        if 'maintenance' in data:
            config['maintenance'] = data['maintenance']
        if 'freefire_maintenance' in data:
            config['freefire_maintenance'] = data['freefire_maintenance']
        if 'freefire_max_maintenance' in data:
            config['freefire_max_maintenance'] = data['freefire_max_maintenance']
        
        save_config(config)
        return jsonify({"success": True, "message": "Maintenance status updated"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/update/app', methods=['POST'])
@login_required
def update_app_info():
    try:
        data = request.json
        config = load_config()
        
        if 'update_available' in data:
            config['update_available'] = data['update_available']
        if 'update_version' in data:
            config['update_version'] = data['update_version']
        if 'update_changelog' in data:
            config['update_changelog'] = data['update_changelog']
        if 'update_url' in data:
            config['update_url'] = data['update_url']
        
        save_config(config)
        return jsonify({"success": True, "message": "App info updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/asset/update', methods=['POST'])
@login_required
def update_asset():
    try:
        data = request.json
        config = load_config()
        assets = config.get('assets', [])
        
        if 'name' in data and 'url' in data:
            for asset in assets:
                if asset.get('name') == data['name']:
                    asset['url'] = data['url']
                    config['assets'] = assets
                    save_config(config)
                    return jsonify({"success": True, "message": "Asset updated"})
            
            assets.append({"name": data['name'], "url": data['url']})
            config['assets'] = assets
            save_config(config)
            return jsonify({"success": True, "message": "Asset added"})
        
        return jsonify({"success": False, "message": "Missing name or url"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/update/master_key', methods=['POST'])
@login_required
def update_master_key():
    try:
        data = request.json
        config = load_config()
        
        if 'master_key' in data:
            config['master_key'] = data['master_key']
        if 'master_key_expiry' in data:
            config['master_key_expiry'] = data['master_key_expiry']
        
        save_config(config)
        return jsonify({"success": True, "message": "Master key updated"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# =============== WEB ROUTES ===============

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    create_admin('admin', 'admin123')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_admin(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error='Invalid credentials')
    
    return render_template_string(LOGIN_TEMPLATE, error=None)

@app.route('/dashboard')
@login_required
def dashboard():
    config = load_config()
    username = session.get('username', 'Admin')
    return render_template_string(DASHBOARD_TEMPLATE, config=config, username=username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# =============== TEMPLATES ===============

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
        body{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;justify-content:center;align-items:center}
        .login-container{background:white;padding:3rem 2.5rem;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.3);width:100%;max-width:420px}
        .login-header{text-align:center;margin-bottom:2rem}
        .login-header h1{font-size:2rem;color:#2d3748;font-weight:700}
        .login-header p{color:#718096;margin-top:0.5rem;font-size:0.95rem}
        .form-group{margin-bottom:1.5rem}
        .form-group label{display:block;margin-bottom:0.5rem;color:#2d3748;font-weight:600;font-size:0.9rem;text-transform:uppercase;letter-spacing:0.5px}
        .form-group input{width:100%;padding:0.875rem 1rem;border:2px solid #e2e8f0;border-radius:10px;font-size:1rem;transition:all 0.3s ease;background:#f7fafc}
        .form-group input:focus{outline:none;border-color:#667eea;background:white;box-shadow:0 0 0 3px rgba(102,126,234,0.1)}
        .login-btn{width:100%;padding:0.875rem;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:10px;font-size:1rem;font-weight:600;cursor:pointer;transition:all 0.3s ease;text-transform:uppercase;letter-spacing:1px}
        .login-btn:hover{transform:translateY(-2px);box-shadow:0 10px 20px rgba(102,126,234,0.3)}
        .error-message{background:#fed7d7;color:#c53030;padding:0.75rem 1rem;border-radius:10px;margin-bottom:1.5rem;text-align:center;font-weight:500;border-left:4px solid #fc8181}
        .login-footer{margin-top:1.5rem;text-align:center;color:#a0aec0;font-size:0.85rem}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>Admin Panel</h1>
            <p>Secure access to configuration management</p>
        </div>
        {% if error %}
        <div class="error-message">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter username" required autofocus>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="login-btn">Sign In</button>
        </form>
        <div class="login-footer">Secure Administration Interface</div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administration Dashboard</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
        body{background:#f0f2f5;padding:20px}
        .container{max-width:1440px;margin:0 auto}
        
        .header{background:white;padding:1.5rem 2rem;border-radius:12px;box-shadow:0 2px 4px rgba(0,0,0,0.05);margin-bottom:2rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
        .header h1{color:#1a202c;font-size:1.5rem;font-weight:600}
        .header-user{display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
        .header-user span{color:#4a5568;font-weight:500}
        .logout-btn{padding:0.5rem 1.25rem;background:#e53e3e;color:white;border:none;border-radius:6px;cursor:pointer;text-decoration:none;font-weight:500;transition:background 0.2s}
        .logout-btn:hover{background:#c53030}
        
        .stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.5rem;margin-bottom:2rem}
        .stat-card{background:white;padding:1.5rem;border-radius:12px;box-shadow:0 2px 4px rgba(0,0,0,0.05)}
        .stat-card h3{color:#718096;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:0.5rem}
        .stat-card .value{font-size:1.75rem;font-weight:700;color:#1a202c}
        
        /* Tabs */
        .tabs{display:flex;gap:0.5rem;margin-bottom:1.5rem;flex-wrap:wrap;background:white;padding:0.5rem;border-radius:12px;box-shadow:0 2px 4px rgba(0,0,0,0.05)}
        .tab-btn{padding:0.7rem 1.5rem;border:none;background:transparent;border-radius:8px;cursor:pointer;font-weight:500;color:#4a5568;transition:all 0.3s;font-size:0.9rem}
        .tab-btn:hover{background:#edf2f7;color:#1a202c}
        .tab-btn.active{background:#667eea;color:white;box-shadow:0 4px 12px rgba(102,126,234,0.3)}
        .tab-content{display:none}
        .tab-content.active{display:block}
        
        .section{background:white;padding:1.5rem;border-radius:12px;box-shadow:0 2px 4px rgba(0,0,0,0.05);margin-bottom:1.5rem}
        .section h2{color:#1a202c;font-size:1.1rem;margin-bottom:1.25rem;font-weight:600;border-bottom:2px solid #edf2f7;padding-bottom:0.75rem}
        
        .button-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:1rem}
        .button-card{background:#f7fafc;padding:1rem 1.25rem;border-radius:8px;border-left:4px solid #48bb78;transition:all 0.2s}
        .button-card:hover{background:#edf2f7;transform:translateX(4px)}
        .button-card .name{font-weight:600;color:#1a202c;margin-bottom:0.25rem;font-size:1rem}
        .button-card .id{font-size:0.7rem;color:#a0aec0;margin-bottom:0.25rem;font-family:monospace}
        .button-card .url{font-size:0.65rem;color:#718096;margin-bottom:0.5rem;word-break:break-all;font-family:monospace;background:#edf2f7;padding:0.2rem 0.5rem;border-radius:4px}
        .button-card .status{display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:0.75rem}
        
        .badge{padding:0.15rem 0.6rem;border-radius:12px;font-size:0.7rem;font-weight:600;display:inline-block}
        .badge-success{background:#c6f6d5;color:#22543d}
        .badge-danger{background:#fed7d7;color:#742a2a}
        .badge-warning{background:#fefcbf;color:#744210}
        .badge-info{background:#bee3f8;color:#2a4365}
        
        .control-group{display:flex;gap:0.5rem;flex-wrap:wrap}
        .btn{padding:0.3rem 0.7rem;border:none;border-radius:4px;cursor:pointer;font-size:0.7rem;font-weight:600;transition:all 0.2s}
        .btn:hover{transform:scale(1.05);box-shadow:0 2px 8px rgba(0,0,0,0.15)}
        .btn-enable{background:#48bb78;color:white}
        .btn-enable:hover{background:#38a169}
        .btn-disable{background:#fc8181;color:white}
        .btn-disable:hover{background:#f56565}
        .btn-maintenance{background:#ed8936;color:white}
        .btn-maintenance:hover{background:#dd6b20}
        .btn-active{background:#4299e1;color:white}
        .btn-active:hover{background:#3182ce}
        .btn-edit{background:#9f7aea;color:white}
        .btn-edit:hover{background:#805ad5}
        
        .maintenance-toggle{background:#edf2f7;border:2px solid #e2e8f0;padding:0.5rem 1rem;border-radius:6px;cursor:pointer;font-weight:500;color:#2d3748;transition:all 0.2s}
        .maintenance-toggle:hover{background:#e2e8f0}
        
        .config-input{width:100%;padding:0.7rem;border:2px solid #e2e8f0;border-radius:6px;margin-top:0.5rem;font-size:0.9rem;background:#f7fafc;transition:all 0.2s}
        .config-input:focus{outline:none;border-color:#667eea;background:white}
        
        .save-btn{background:#667eea;color:white;border:none;padding:0.5rem 1.5rem;border-radius:6px;cursor:pointer;font-weight:500;margin-top:0.5rem;transition:all 0.2s}
        .save-btn:hover{background:#5a67d8;transform:translateY(-1px);box-shadow:0 4px 12px rgba(102,126,234,0.3)}
        
        .json-view{background:#2d3748;padding:1.25rem;border-radius:8px;overflow:auto;max-height:500px;font-size:0.75rem;color:#f7fafc;font-family:'Courier New',monospace;line-height:1.6}
        .refresh-btn{background:#48bb78;color:white;border:none;padding:0.5rem 1.5rem;border-radius:6px;cursor:pointer;font-weight:500;margin-bottom:1rem;transition:all 0.2s}
        .refresh-btn:hover{background:#38a169;transform:translateY(-1px)}
        
        .status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}
        .status-dot.online{background:#48bb78}
        .status-dot.maintenance{background:#fc8181}
        .status-dot.active{background:#48bb78}
        .status-dot.inactive{background:#a0aec0}
        
        .flex-row{display:flex;gap:1rem;flex-wrap:wrap;align-items:center}
        .flex-col{display:flex;flex-direction:column;gap:0.5rem}
        
        .edit-modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:999;justify-content:center;align-items:center}
        .edit-modal-content{background:white;padding:2rem;border-radius:12px;max-width:500px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
        .edit-modal-content h3{margin-bottom:1rem;color:#1a202c;font-weight:600}
        .edit-modal-content label{display:block;margin-bottom:0.25rem;color:#4a5568;font-weight:500;font-size:0.85rem}
        .edit-modal-content input{width:100%;padding:0.7rem;border:2px solid #e2e8f0;border-radius:6px;margin-bottom:0.75rem;font-size:0.9rem;transition:all 0.2s}
        .edit-modal-content input:focus{outline:none;border-color:#667eea}
        .edit-modal-content .modal-actions{display:flex;gap:0.5rem;justify-content:flex-end;margin-top:1rem}
        .edit-modal-content .modal-actions button{padding:0.5rem 1.5rem;border:none;border-radius:6px;cursor:pointer;font-weight:500}
        .edit-modal-content .modal-actions .save{background:#48bb78;color:white}
        .edit-modal-content .modal-actions .save:hover{background:#38a169}
        .edit-modal-content .modal-actions .cancel{background:#fc8181;color:white}
        .edit-modal-content .modal-actions .cancel:hover{background:#f56565}
        
        .toast{position:fixed;bottom:20px;right:20px;background:#1a202c;color:white;padding:0.75rem 1.5rem;border-radius:8px;z-index:1000;box-shadow:0 4px 12px rgba(0,0,0,0.2);display:none;animation:slideIn 0.3s ease}
        .toast.success{background:#48bb78}
        .toast.error{background:#fc8181}
        @keyframes slideIn{from{transform:translateY(100px);opacity:0}to{transform:translateY(0);opacity:1}}
        
        .empty-state{text-align:center;padding:2rem;color:#718096;font-size:0.95rem}
        
        @media(max-width:768px){.header{flex-direction:column;gap:1rem;align-items:stretch}.header-user{justify-content:space-between}.button-grid{grid-template-columns:1fr}.tabs{flex-direction:column}.tab-btn{width:100%;text-align:center}}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Administration Dashboard</h1>
            <div class="header-user">
                <span>Welcome, {{ username }}</span>
                <a href="/logout" class="logout-btn">Sign Out</a>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card"><h3>FreeFire Buttons</h3><div class="value">{{ config.freefire_buttons|length }}</div></div>
            <div class="stat-card"><h3>FreeFire Max Buttons</h3><div class="value">{{ config.freefire_max_buttons|length }}</div></div>
            <div class="stat-card"><h3>Root Libraries</h3><div class="value">{{ config.root_libs|length }}</div></div>
            <div class="stat-card"><h3>Assets</h3><div class="value">{{ config.assets|length }}</div></div>
        </div>

        <!-- Tabs -->
        <div class="tabs">
            <button class="tab-btn active" data-tab="tab-maintenance">Maintenance</button>
            <button class="tab-btn" data-tab="tab-freefire">FreeFire</button>
            <button class="tab-btn" data-tab="tab-freefiremax">FreeFire Max</button>
            <button class="tab-btn" data-tab="tab-rootlibs">Root Libraries</button>
            <button class="tab-btn" data-tab="tab-update">Update</button>
            <button class="tab-btn" data-tab="tab-config">Configuration</button>
        </div>

        <!-- Tab: Maintenance -->
        <div id="tab-maintenance" class="tab-content active">
            <div class="section">
                <h2>Maintenance Controls</h2>
                <div class="flex-row">
                    <button class="maintenance-toggle" onclick="toggleMaintenance('maintenance', {{ config.maintenance|lower }})">
                        <span class="status-dot {{ 'online' if not config.maintenance else 'maintenance' }}"></span>
                        Application: {{ 'Online' if not config.maintenance else 'Maintenance' }}
                    </button>
                    <button class="maintenance-toggle" onclick="toggleMaintenance('freefire_maintenance', {{ config.freefire_maintenance|lower }})">
                        <span class="status-dot {{ 'online' if not config.freefire_maintenance else 'maintenance' }}"></span>
                        FreeFire: {{ 'Online' if not config.freefire_maintenance else 'Maintenance' }}
                    </button>
                    <button class="maintenance-toggle" onclick="toggleMaintenance('freefire_max_maintenance', {{ config.freefire_max_maintenance|lower }})">
                        <span class="status-dot {{ 'online' if not config.freefire_max_maintenance else 'maintenance' }}"></span>
                        FreeFire Max: {{ 'Online' if not config.freefire_max_maintenance else 'Maintenance' }}
                    </button>
                </div>
            </div>

            <div class="section">
                <h2>Master Key Controls</h2>
                <div class="flex-col">
                    <input class="config-input" id="master_key" placeholder="Master Key" value="{{ config.master_key }}">
                    <input class="config-input" id="master_key_expiry" placeholder="Expiry Date" value="{{ config.master_key_expiry }}">
                    <button class="save-btn" onclick="updateMasterKey()">Update Master Key</button>
                </div>
            </div>
        </div>

        <!-- Tab: FreeFire -->
        <div id="tab-freefire" class="tab-content">
            <div class="section">
                <h2>FreeFire Buttons</h2>
                <div class="button-grid">
                    {% for button in config.freefire_buttons %}
                    <div class="button-card" style="border-left-color: {{ '#48bb78' if button.enabled else '#fc8181' }}">
                        <div class="name">{{ button.name }}</div>
                        <div class="id">ID: {{ button.id }}</div>
                        <div class="url">URL: {{ button.url }}</div>
                        <div class="status">
                            <span class="badge {{ 'badge-success' if button.enabled else 'badge-danger' }}">
                                <span class="status-dot {{ 'active' if button.enabled else 'inactive' }}"></span>
                                {{ 'Enabled' if button.enabled else 'Disabled' }}
                            </span>
                            <span class="badge {{ 'badge-warning' if button.maintenance else 'badge-info' }}">
                                <span class="status-dot {{ 'maintenance' if button.maintenance else 'active' }}"></span>
                                {{ 'Maintenance' if button.maintenance else 'Active' }}
                            </span>
                        </div>
                        <div class="control-group">
                            <button class="btn {{ 'btn-enable' if not button.enabled else 'btn-disable' }}" 
                                    onclick="toggleButton('freefire', '{{ button.id }}', {{ not button.enabled|lower }}, {{ button.maintenance|lower }})">
                                {{ 'Enable' if not button.enabled else 'Disable' }}
                            </button>
                            <button class="btn {{ 'btn-active' if button.maintenance else 'btn-maintenance' }}"
                                    onclick="toggleMaintenanceButton('freefire', '{{ button.id }}', {{ not button.maintenance|lower }}, {{ button.enabled|lower }})">
                                {{ 'Set Active' if button.maintenance else 'Set Maintenance' }}
                            </button>
                            <button class="btn btn-edit" onclick="openEditModal('freefire', '{{ button.id }}', '{{ button.name }}', '{{ button.url }}')">Edit</button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Tab: FreeFire Max -->
        <div id="tab-freefiremax" class="tab-content">
            <div class="section">
                <h2>FreeFire Max Buttons</h2>
                <div class="button-grid">
                    {% for button in config.freefire_max_buttons %}
                    <div class="button-card" style="border-left-color: {{ '#48bb78' if button.enabled else '#fc8181' }}">
                        <div class="name">{{ button.name }}</div>
                        <div class="id">ID: {{ button.id }}</div>
                        <div class="url">URL: {{ button.url }}</div>
                        <div class="status">
                            <span class="badge {{ 'badge-success' if button.enabled else 'badge-danger' }}">
                                <span class="status-dot {{ 'active' if button.enabled else 'inactive' }}"></span>
                                {{ 'Enabled' if button.enabled else 'Disabled' }}
                            </span>
                            <span class="badge {{ 'badge-warning' if button.maintenance else 'badge-info' }}">
                                <span class="status-dot {{ 'maintenance' if button.maintenance else 'active' }}"></span>
                                {{ 'Maintenance' if button.maintenance else 'Active' }}
                            </span>
                        </div>
                        <div class="control-group">
                            <button class="btn {{ 'btn-enable' if not button.enabled else 'btn-disable' }}" 
                                    onclick="toggleButton('freefire_max', '{{ button.id }}', {{ not button.enabled|lower }}, {{ button.maintenance|lower }})">
                                {{ 'Enable' if not button.enabled else 'Disable' }}
                            </button>
                            <button class="btn {{ 'btn-active' if button.maintenance else 'btn-maintenance' }}"
                                    onclick="toggleMaintenanceButton('freefire_max', '{{ button.id }}', {{ not button.maintenance|lower }}, {{ button.enabled|lower }})">
                                {{ 'Set Active' if button.maintenance else 'Set Maintenance' }}
                            </button>
                            <button class="btn btn-edit" onclick="openEditModal('freefire_max', '{{ button.id }}', '{{ button.name }}', '{{ button.url }}')">Edit</button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Tab: Root Libraries -->
        <div id="tab-rootlibs" class="tab-content">
            <div class="section">
                <h2>Root Libraries</h2>
                <div class="button-grid">
                    {% for lib in config.root_libs %}
                    <div class="button-card" style="border-left-color: {{ '#48bb78' if lib.enabled else '#fc8181' }}">
                        <div class="name">{{ lib.name }}</div>
                        <div class="id">ID: {{ lib.id }}</div>
                        <div class="url">URL: {{ lib.url }}</div>
                        <div style="font-size:0.7rem;color:#718096;margin-bottom:0.5rem">Path: {{ lib.lib_path }} | Arch: {{ lib.arch }}</div>
                        <div class="status">
                            <span class="badge {{ 'badge-success' if lib.enabled else 'badge-danger' }}">
                                <span class="status-dot {{ 'active' if lib.enabled else 'inactive' }}"></span>
                                {{ 'Enabled' if lib.enabled else 'Disabled' }}
                            </span>
                            <span class="badge {{ 'badge-warning' if lib.maintenance else 'badge-info' }}">
                                <span class="status-dot {{ 'maintenance' if lib.maintenance else 'active' }}"></span>
                                {{ 'Maintenance' if lib.maintenance else 'Active' }}
                            </span>
                        </div>
                        <div class="control-group">
                            <button class="btn {{ 'btn-enable' if not lib.enabled else 'btn-disable' }}" 
                                    onclick="toggleButton('root_libs', '{{ lib.id }}', {{ not lib.enabled|lower }}, {{ lib.maintenance|lower }})">
                                {{ 'Enable' if not lib.enabled else 'Disable' }}
                            </button>
                            <button class="btn {{ 'btn-active' if lib.maintenance else 'btn-maintenance' }}"
                                    onclick="toggleMaintenanceButton('root_libs', '{{ lib.id }}', {{ not lib.maintenance|lower }}, {{ lib.enabled|lower }})">
                                {{ 'Set Active' if lib.maintenance else 'Set Maintenance' }}
                            </button>
                            <button class="btn btn-edit" onclick="openEditModal('root_libs', '{{ lib.id }}', '{{ lib.name }}', '{{ lib.url }}')">Edit</button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Tab: Update -->
        <div id="tab-update" class="tab-content">
            <div class="section">
                <h2>Application Update Controls</h2>
                <div class="flex-row" style="margin-bottom:1rem">
                    <button class="maintenance-toggle" onclick="toggleUpdate()">
                        <span class="status-dot {{ 'online' if config.update_available else 'inactive' }}"></span>
                        Update: {{ 'Available' if config.update_available else 'Not Available' }}
                    </button>
                </div>
                <div class="flex-col">
                    <input class="config-input" id="update_version" placeholder="Update Version" value="{{ config.update_version }}">
                    <input class="config-input" id="update_url" placeholder="Update URL" value="{{ config.update_url }}">
                    <textarea class="config-input" id="update_changelog" rows="3" placeholder="Update Changelog">{{ config.update_changelog }}</textarea>
                    <button class="save-btn" onclick="saveUpdateInfo()">Save Update Information</button>
                </div>
            </div>

            <div class="section">
                <h2>Asset Management</h2>
                <div class="flex-col">
                    <input class="config-input" id="asset_name" placeholder="Asset Name (e.g. bg.mp4)">
                    <input class="config-input" id="asset_url" placeholder="Asset URL">
                    <button class="save-btn" onclick="updateAsset()">Update or Add Asset</button>
                </div>
                <div style="margin-top:1rem">
                    <h3 style="font-size:0.9rem;color:#4a5568;margin-bottom:0.5rem">Current Assets:</h3>
                    {% for asset in config.assets %}
                    <div style="background:#f7fafc;padding:0.5rem;border-radius:4px;margin-bottom:0.25rem;font-size:0.8rem">
                        <strong>{{ asset.name }}</strong>: {{ asset.url }}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Tab: Configuration -->
        <div id="tab-config" class="tab-content">
            <div class="section">
                <h2>Configuration Viewer</h2>
                <button class="refresh-btn" onclick="refreshConfig()">Refresh Configuration</button>
                <div class="json-view" id="configView">{{ config|tojson|safe }}</div>
            </div>
        </div>
    </div>

    <!-- Edit Modal -->
    <div class="edit-modal" id="editModal">
        <div class="edit-modal-content">
            <h3>Edit Button Configuration</h3>
            <input type="hidden" id="edit_type">
            <input type="hidden" id="edit_id">
            <label>Button Name</label>
            <input id="edit_name" placeholder="Enter button name">
            <label>Button URL</label>
            <input id="edit_url" placeholder="Enter button URL">
            <div class="modal-actions">
                <button class="cancel" onclick="closeEditModal()">Cancel</button>
                <button class="save" onclick="saveEdit()">Save Changes</button>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div class="toast" id="toast"></div>

    <script>
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                document.getElementById(this.dataset.tab).classList.add('active');
            });
        });

        function showToast(message, type) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast ' + type;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 3000);
        }

        async function toggleButton(type, id, enabled, maintenance) {
            try {
                const response = await fetch(`/api/button/toggle/${type}/${id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({enabled: enabled, maintenance: maintenance})
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Button toggled successfully', 'success');
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        async function toggleMaintenanceButton(type, id, maintenance, enabled) {
            try {
                const response = await fetch(`/api/button/toggle/${type}/${id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({enabled: enabled, maintenance: maintenance})
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Maintenance status updated', 'success');
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        async function toggleMaintenance(type, current) {
            try {
                const response = await fetch('/api/maintenance/toggle', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({[type]: !current})
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Maintenance status updated', 'success');
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        async function toggleUpdate() {
            try {
                const current = {{ config.update_available|lower }};
                const response = await fetch('/api/update/app', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({update_available: !current})
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Update status toggled', 'success');
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        async function saveUpdateInfo() {
            const version = document.getElementById('update_version').value;
            const url = document.getElementById('update_url').value;
            const changelog = document.getElementById('update_changelog').value;
            
            try {
                const response = await fetch('/api/update/app', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        update_version: version,
                        update_url: url,
                        update_changelog: changelog
                    })
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Update information saved', 'success');
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        async function updateMasterKey() {
            const master_key = document.getElementById('master_key').value;
            const master_key_expiry = document.getElementById('master_key_expiry').value;
            
            try {
                const response = await fetch('/api/update/master_key', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        master_key: master_key,
                        master_key_expiry: master_key_expiry
                    })
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Master key updated', 'success');
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        async function updateAsset() {
            const name = document.getElementById('asset_name').value;
            const url = document.getElementById('asset_url').value;
            
            if (!name || !url) {
                showToast('Please enter both name and URL', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/asset/update', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name: name, url: url})
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Asset updated successfully', 'success');
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        function openEditModal(type, id, name, url) {
            document.getElementById('edit_type').value = type;
            document.getElementById('edit_id').value = id;
            document.getElementById('edit_name').value = name;
            document.getElementById('edit_url').value = url;
            document.getElementById('editModal').style.display = 'flex';
        }

        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
        }

        async function saveEdit() {
            const type = document.getElementById('edit_type').value;
            const id = document.getElementById('edit_id').value;
            const name = document.getElementById('edit_name').value;
            const url = document.getElementById('edit_url').value;
            
            try {
                const response = await fetch(`/api/button/update/${type}/${id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name: name, url: url})
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Button updated successfully', 'success');
                    closeEditModal();
                    setTimeout(() => location.reload(), 500);
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            } catch (error) {
                showToast('Error: ' + error.message, 'error');
            }
        }

        async function refreshConfig() {
            try {
                const response = await fetch('/api/config');
                const data = await response.json();
                document.getElementById('configView').textContent = JSON.stringify(data, null, 2);
                showToast('Configuration refreshed', 'success');
            } catch (error) {
                showToast('Error refreshing config', 'error');
            }
        }

        setInterval(refreshConfig, 30000);

        window.onclick = function(event) {
            const modal = document.getElementById('editModal');
            if (event.target == modal) {
                closeEditModal();
            }
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    create_admin('admin', 'admin123')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)