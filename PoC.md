# Proof of Concept (PoC): PHP2Shell Targeted Honeypot

## Objective
The goal of this Proof of Concept is to demonstrate the honeypot's ability to intercept, classify, and log the two main phases of the PHP2Shell (CVE-2026-109618/19) memory corruption vulnerability, without the host Python environment crashing.

## 1. Environment Setup
The honeypot is deployed in an isolated Docker container to prevent any host compromise. 

To start the sensor, the following command is executed on the host machine, mapping port 8080 and establishing a persistent volume for the logs:

```bash
docker run --rm -p 8080:8080 -v "${PWD}/logs:/app/logs" --name rpg_sensor php2shell-honeypot
```

![Honeypot Initialization](./img/01_startup.png)
*(Note: Replace with a screenshot of the Docker container starting up and guarding port 8080)*

## 2. Attack Simulation

We simulate the attack using Windows PowerShell to send crafted HTTP requests directly to the sensor.

### Phase 1: OOM Trigger (State Corruption)
The attacker attempts to exhaust the 128MB PHP memory limit by sending an artificially inflated `Content-Length` header. 

```powershell
Invoke-WebRequest -Uri "http://localhost:8080/index.php" -Method Post -Headers @{"Content-Length"="60000000"} -UserAgent "Wiz-Research-Probe" -UseBasicParsing
```

**Expected Result:** The honeypot detects the anomaly in the header, drops the payload to save its own memory, and logs a `PHP2SHELL_PHASE1_OOM` alert.

### Phase 2: Use-After-Free (UAF) Injection
Once the PHP engine is left in a stale state, the attacker attempts to inject raw memory pointers or shellcode (represented here by the hexadecimal equivalent of 'A' padding).

```powershell
Invoke-WebRequest -Uri "http://localhost:8080/index.php" -Method Post -Body "AAAAAAAAAAAAAAAAAAAA" -UserAgent "Wiz-Research-Probe" -UseBasicParsing
```

![PowerShell Execution](./img/02_powershell_attack.png)
*(Note: Replace with the screenshot of your PowerShell terminal executing the command and receiving the 200 OK)*

## 3. Results & Visualization

As soon as the Phase 2 payload is received, the `ExploitSignatures` engine intercepts the binary padding. Instead of executing it, the honeypot parses the Threat Intelligence data and outputs the Gamified Battle Log to the console.

![RPG Battle Log Output](./img/03_battle_log.png)
*(Note: Replace with a screenshot of the Docker terminal showing the BOSS ENCOUNTER log in real-time)*

### Persistent Artifacts
Even if the Docker container is destroyed, the logs are safely written to the host machine for post-incident analysis by the Blue Team.

```text
============================================================
[!!! CRITICAL BOSS ENCOUNTER DETECTED !!!] - 2026-10-23 10:35:12
============================================================
[!] PHP2Shell Exploit Chain from IP [172.17.0.1] appeared!
[i] Enemy Gear (User-Agent): Wiz-Research-Probe
[>] ATTACK SIGNATURE: PHP2SHELL_PHASE2_UAF
[>] SENSOR DETAILS: Content-Length: 20 bytes | Binary shellcode or memory padding detected
[*] RESULT: Python Engine unaffected by PHP memory corruption. 0 damage.
[+] +1000 XP (ZERO-DAY BLOCKED)
============================================================
```

## Conclusion
The PoC successfully validates that protocol-level anomalies and raw memory exploitation attempts can be safely intercepted, classified, and persisted using a lightweight, containerized Python sensor.