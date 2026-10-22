import os
import logging
from datetime import datetime
from flask import Flask, request

# ==========================================
# 1. THREAT SIGNATURE ENGINE (WIZ RESEARCH PHP2SHELL)
# ==========================================
class ExploitSignatures:
    """Matches HTTP anomalies against the PHP2Shell (CVE-2026-109618/19) kill chain."""
    
    @staticmethod
    def analyze(req):
        # Phase 1: Out-Of-Memory (OOM) Trigger Attempt
        # Attacker sends a request with a massive Content-Length header to exhaust PHP workers.
        content_length = req.content_length or 0
        if content_length > 50_000_000:
            return "PHP2SHELL_PHASE1_OOM"
            
        # Phase 2: Use-After-Free (UAF) Exploitation
        # Attacker sends raw binary, manipulated pointers, or NOP sleds to control memory.
        raw_payload = req.get_data(as_text=False)
        if b'\x90\x90\x90\x90' in raw_payload or b'\x41\x41\x41\x41' in raw_payload or b'AAAA' in raw_payload:
            return "PHP2SHELL_PHASE2_UAF"
            
        # Catch standard web attacks (e.g., ?cmd=ls)
        if req.args or req.form:
            return "GENERIC_WEB_ATTACK"
            
        return "UNKNOWN_SCAN"

# ==========================================
# 2. RPG LOGGER ENGINE
# ==========================================
class RPGBattleLogger:
    """Formats raw Threat Intelligence data into an RPG battle log and saves it."""
    
    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "battle_log.txt")

    @staticmethod
    def initialize():
        if not os.path.exists(RPGBattleLogger.LOG_DIR):
            os.makedirs(RPGBattleLogger.LOG_DIR)

    @staticmethod
    def log_encounter(ip, user_agent, threat_type, details):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if "PHP2SHELL" in threat_type:
            header = "[!!! CRITICAL BOSS ENCOUNTER DETECTED !!!]"
            enemy = f"PHP2Shell Exploit Chain from IP [{ip}]"
            xp = "+1000 XP (ZERO-DAY BLOCKED)"
        else:
            header = "[ BATTLE ENGAGED ]"
            enemy = f"Script Kiddie from IP [{ip}]"
            xp = "+50 XP"

        log_entry = (
            f"\n{'='*60}\n"
            f"{header} - {timestamp}\n"
            f"{'='*60}\n"
            f"[!] {enemy} appeared!\n"
            f"[i] Enemy Gear (User-Agent): {user_agent}\n"
            f"[>] ATTACK SIGNATURE: {threat_type}\n"
            f"[>] SENSOR DETAILS: {details}\n"
            f"[*] RESULT: Python Engine unaffected by PHP memory corruption. 0 damage.\n"
            f"[+] {xp}\n"
            f"{'='*60}\n"
        )
        
        print(log_entry, end="")
        with open(RPGBattleLogger.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)

# ==========================================
# 3. FLASK SERVER SETUP
# ==========================================
app = Flask(__name__)

# Disable default Flask access logs to keep the RPG console clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

RPGBattleLogger.initialize()

@app.after_request
def modify_server_headers(response):
    """Spoofs headers to pretend this is a vulnerable PHP environment."""
    response.headers['Server'] = 'Apache/2.4.41 (Ubuntu)'
    response.headers['X-Powered-By'] = 'PHP/8.2.0'
    return response

# ==========================================
# 4. THE TRAP (PHP2SHELL SENSOR)
# ==========================================
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.php', methods=['GET', 'POST'])
@app.route('/login.php', methods=['GET', 'POST'])
def vulnerable_endpoint():
    """Intercepts attacks, extracts IoCs, and runs signature analysis."""
    
    attacker_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Analyze the request against our exploit signatures
    threat_type = ExploitSignatures.analyze(request)
    
    # If a threat is detected, extract details and log the encounter
    if threat_type != "UNKNOWN_SCAN":
        details = f"Content-Length: {request.content_length} bytes"
        if threat_type == "PHP2SHELL_PHASE2_UAF":
            details += " | Binary shellcode or memory padding detected"
            
        RPGBattleLogger.log_encounter(attacker_ip, user_agent, threat_type, details)

    # Return a silent 200 OK so the attacker believes the exploit worked
    return "", 200

# ==========================================
# 5. STARTUP
# ==========================================
if __name__ == '__main__':
    print("[SYSTEM] Targeted Honeypot Initialized: CVE-2026-109618/19 (PHP2Shell)")
    print(f"[SYSTEM] Logging to {RPGBattleLogger.LOG_FILE}")
    print("[SYSTEM] Guarding port 8080...")
    app.run(host='0.0.0.0', port=8080)