# 🧪 Security Analyst Interactive Lab Suite

Welcome! This application is built for you to practice web security analysis on a realistic target.

## 🚀 Getting Started

To run the lab suite on your local machine, follow these steps:

### 1. Prerequisites
Make sure you have **Python 3** installed.

### 2. Install Dependencies
Run the following command in the `vulnerable-app` directory:
```bash
pip install flask requests
```

### 3. Start the Server
Run the application:
```bash
python3 app.py
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
