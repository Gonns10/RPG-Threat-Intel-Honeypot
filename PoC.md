# Proof of Concept (PoC): PHP2Shell Targeted Honeypot

## Objective
The goal of this Proof of Concept is to demonstrate the honeypot's ability to intercept, classify, and log the two main phases of the PHP2Shell (CVE-2026-109618/19) memory corruption vulnerability, without the host Python environment crashing.

## 1. Environment Setup
The honeypot is deployed in an isolated Docker container to prevent any host compromise. 

First, we build the isolated Docker image and start the honeypot, mapping port 8080 and the persistent logs volume:

```bash
docker build -t php2shell-honeypot .

docker run --rm -p 8080:8080 -v "${PWD}/logs:/app/logs" --name rpg_sensor php2shell-honeypot

```


![[Pasted image 20261025200220.png]]

## 2. Attack Simulation

We simulate the attack using Windows PowerShell to send crafted HTTP requests directly to the sensor.

### Phase 1: OOM Trigger (State Corruption)
The attacker attempts to exhaust the 128MB PHP memory limit by sending an artificially inflated `Content-Length` header. 

We use `curl.exe` to bypass PowerShell's native header recalculations and force a massive, fake `Content-Length` (150MB) with an empty body, simulating the Out-Of-Memory trigger.

```powershell
curl.exe -X POST -H "Content-Length: 150000000" -A "Wiz-Research-Probe" http://localhost:8080/index.php
```

**Expected Result:** The honeypot detects the anomaly in the header, drops the payload to save its own memory, and logs a `PHP2SHELL_PHASE1_OOM` alert.

![[Pasted image 20261025200755.png]]

### Phase 2: Use-After-Free (UAF) Injection
Once the PHP engine is left in a stale state, the attacker attempts to inject raw memory pointers or shellcode (represented here by the hexadecimal equivalent of 'A' padding).

```powershell
Invoke-WebRequest -Uri "http://localhost:8080/index.php" -Method Post -Body "AAAAAAAAAAAAAAAAAAAA" -UserAgent "Wiz-Research-Probe" -UseBasicParsing
```

![[Pasted image 20261025201112.png]]


## 3. Results & Visualization

As soon as the Phase 2 payload is received, the `ExploitSignatures` engine intercepts the binary padding. Instead of executing it, the honeypot parses the Threat Intelligence data and outputs the Gamified Battle Log to the console.

![[Pasted image 20261025201131.png]]

### Persistent Artifacts
Even if the Docker container is destroyed, the logs are safely written to the host machine for post-incident analysis by the Blue Team.

![[Pasted image 20261025201302.png]]
## Conclusion
The PoC successfully validates that protocol-level anomalies and raw memory exploitation attempts can be safely intercepted, classified, and persisted using a lightweight, containerized Python sensor.