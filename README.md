# RPG Threat Intel Honeypot: PHP2Shell Sensor

## Overview
This project is a targeted HTTP honeypot developed to capture in-the-wild exploitation attempts of the recent "PHP2Shell" memory corruption vulnerabilities (CVE-2026-109618, CVE-2026-109619) detailed by Wiz Research. 

While traditional honeypots look for application-level command injection strings, this sensor is engineered to detect the specific HTTP protocol anomalies associated with PHP engine memory exhaustion and Use-After-Free (UAF) exploitation. 

## Why Gamification?
In modern Security Operations Centers (SOCs), alert fatigue is a real issue. This project serves as a creative exercise in **data visualization**. By formatting raw Indicators of Compromise (IoCs) and attack vectors as "RPG encounters", it demonstrates how security event logging can be restructured for better readability and engagement without losing technical rigor.

## Architecture & Detection Logic
The PHP2Shell vulnerability resides in the PHP engine's core C code, specifically triggered during Out-Of-Memory (OOM) aborts. Because this honeypot is built in Python (Flask) and isolated via Docker, it is completely immune to the PHP memory corruption, allowing it to safely observe and log the attack chain without crashing.

The ExploitSignatures engine monitors for the two distinct phases of the exploit:

1. **Phase 1: OOM Trigger (State Corruption)**
   Attackers attempt to exhaust the PHP worker's 128MB limit to force a long jump abort. The honeypot detects this by analyzing anomalous Content-Length headers targeting lightweight endpoints, without actually processing the heavy payload.
2. **Phase 2: Use-After-Free (Memory Injection)**
   Once the stale state is achieved, attackers send raw binary or memory pointers. The honeypot inspects the raw byte stream of POST requests to identify memory padding and shellcode signatures.

## Security & DevSecOps
- **Containerized Isolation:** The honeypot runs inside a lightweight Docker container, completely isolated from the host OS.
- **Principle of Least Privilege:** The Docker container executes the application as a restricted, non-root user to mitigate potential container escape vulnerabilities.
- **Persistent Logging:** Attack logs are safely mapped to the host machine using Docker volumes, ensuring data retention even if the container is destroyed.

## Quick Start

### Prerequisites
- Docker Desktop (or Docker Engine)

### Installation & Execution (Docker Recommended)
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/RPG-Threat-Intel-Honeypot.git](https://github.com/YourUsername/RPG-Threat-Intel-Honeypot.git)
   cd RPG-Threat-Intel-Honeypot

```

2. Build the Docker image:
```bash
docker build -t php2shell-honeypot .

```


3. Run the containerized sensor (maps port 8080 and mounts the logs directory):
```bash
docker run -p 8080:8080 -v ${PWD}/logs:/app/logs --name rpg_sensor php2shell-honeypot

```



## Simulated Testing

To test the detection engine locally using PowerShell:

**Simulate Phase 1 (OOM Trigger):**

```powershell
Invoke-WebRequest -Uri "http://localhost:8080/index.php" -Method Post -Headers @{"Content-Length"="60000000"} -UserAgent "Wiz-Research-Probe" -UseBasicParsing

```

**Simulate Phase 2 (UAF Payload):**

```powershell
Invoke-WebRequest -Uri "http://localhost:8080/index.php" -Method Post -Body "AAAAAAAAAAAAAAAAAAAA" -UserAgent "Wiz-Research-Probe" -UseBasicParsing

```

## Disclaimer

This project is built strictly for educational purposes, Threat Intelligence research, and personal portfolio demonstration. It is meant to be run in a safe, controlled environment. Do not use this code in production networks without proper security hardening.

```

Con esto el proyecto queda 100% cerrado y empaquetado a nivel profesional. 

<FollowUp label="Añadir el proyecto al CV o LinkedIn" query="¿Cómo redacto este proyecto para ponerlo de forma atractiva y profesional en mi currículum y en mi perfil de LinkedIn?"/>

```
