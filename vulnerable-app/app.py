from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import json
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key-that-should-be-leaked-later'

# --- DATA SIMULATION ---
EMPLOYEES = {
    "1": {"name": "Alice Johnson", "role": "Junior Developer", "salary": "70,000$"},
    "2": {"name": "Bob Smith", "role": "Designer", "salary": "65,000$"},
    "100": {"name": "Charlie 'The Boss' CEO", "role": "CEO", "salary": "2,500,000$", "secret": "FLAG{IDOR_MASTER_EXPLORER}"}
}

INTERNAL_STOCK_SERVER = "http://10.0.0.50:8080" # Simulated internal IP

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# --- LEVEL 01 ---

@app.route('/level-01')
def level_01():
    return render_template('level_01.html')

@app.route('/level-01/login', methods=['POST'])
def l1_login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role', 'user')
    
    # Realistic vulnerability: The server checks credentials for normal users,
    # but strictly trusts the 'role' parameter if provided.
    if (username == "wiener" and password == "peter") or (username == "admin" and role == "admin"):
        if role == "admin":
            return render_template('level_01_admin.html', user=username)
        return render_template('level_01_user.html', user=username)
    
    return "Invalid credentials.", 401

@app.route('/level-01/config')
def l1_config():
    config = {
        "DEBUG": True,
        "ENV": "PRODUCTION",
        "API_KEY": "SG_KEY_12345_DEV_ONLY_HIDDEN",
        "MAINTENANCE_LOG": "Found error in auth role logic, need to fix later - Dev Team"
    }
    return jsonify(config)

# --- LEVEL 02 (IDOR) ---

@app.route('/level-02')
def level_02():
    return render_template('level_02.html')

@app.route('/api/employee/<id>')
def get_employee(id):
    if id in EMPLOYEES:
        return jsonify(EMPLOYEES[id])
    return jsonify({"error": "Employee not found"}), 404

# --- LEVEL 03 (SSRF) ---

@app.route('/level-03')
def level_03():
    return render_template('level_03.html')

@app.route('/check-stock', methods=['POST'])
def check_stock():
    stock_url = request.form.get('stockApi')
    
    try:
        if "127.0.0.1" in stock_url or "localhost" in stock_url:
            return "Error: External requests only!", 403
            
        # Simulated response from internal network
        if stock_url == "http://192.168.0.1/admin":
            return "<h1>ADMIN INTERFACE</h1><p>Welcome! Carlos has been deleted. FLAG{SSRF_INTERNAL_PENTEST_INITIATED}</p>"
        
        return f"Fetching data from {stock_url}... (Status: 200 Connection Refused)"
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
