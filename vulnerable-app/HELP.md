# 🧪 Security Analyst Interactive Lab Suite

Welcome! This application is built for you to practice web security analysis on a realistic target.

## 🚀 Getting Started

To run the lab suite on your local machine, follow these steps:

### 1. Prerequisites
Make sure you have **Python 3** installed.

### 2. Install Dependencies
Run the following commands in the `vulnerable-app` directory:
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the Server
Run the application:
```bash
python3 app.py
```

### 3.1 (Optional) Configure like a real app
This lab supports basic environment-based configuration (kept intentionally insecure by default).

- Copy the example file: `env.example`
- Export variables in your shell (or load them via your preferred method), e.g.:

```bash
export SECRET_KEY='super-secret-key-that-should-be-leaked-later'
export HOST='127.0.0.1'
export PORT='5000'
export FLASK_DEBUG='1'
```

### 4. Access the Lab
Open your browser and navigate to:
**http://127.0.0.1:5000**

---

## 🎯 Your Mission
Explore the site and find the vulnerabilities in each level. Use a tool like **Burp Suite** to intercept traffic and analyze hidden parameters.

- **Level 01:** Find a way to log in as the administrator.
- **Level 02:** Access a sensitive employee profile that isn't listed.
- **Level 03:** Bypass network restrictions to access an internal admin interface at `http://192.168.0.1/admin`.

Good luck, Analyst! 🕵️‍♂️
