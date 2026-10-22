# RPG Threat Intel Honeypot

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Blue%20Team-red.svg)

## Overview
**RPG Threat Intel Honeypot** is a lightweight, Proof-of-Concept (PoC) HTTP honeypot designed to intercept and log automated web attacks (like RCE or Command Injection attempts targeting PHP endpoints). 

Instead of traditional, hard-to-read server logs, this project parses inbound attack data (IPs, User-Agents, and Payloads) and translates them into a **Gamified Turn-Based RPG Battle Log**. This provides a unique, highly readable visualization of Threat Intelligence (TI) data.

## Why Gamification?
In modern Security Operations Centers (SOCs), alert fatigue is a real issue. This project serves as a creative exercise in **data visualization**. By formatting raw Indicators of Compromise (IoCs) and attack vectors as "RPG encounters", it demonstrates how security event logging can be restructured for better readability and engagement without losing technical rigor.

## Features
- **Endpoint Spoofing:** Simulates classic vulnerable endpoints (e.g., `/?cmd=`, `/index.php`).
- **Header Manipulation:** Spoofs HTTP response headers to masquerade as an outdated Apache/PHP server.
- **Payload Interception:** Safely catches GET/POST parameters without execution.
- **IoC Gathering:** Extracts and logs Attacker IP, Timestamp, User-Agent, and exact injection payloads.
- **Custom Event Logger:** Outputs terminal logs styled as retro RPG battles.

## Quick Start

### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/RPG-Threat-Intel-Honeypot.git](https://github.com/YourUsername/RPG-Threat-Intel-Honeypot.git)
   cd RPG-Threat-Intel-Honeypot
   
Install dependencies:

   ```bash
   pip install -r requirements.txt

   ```
   Run the honeypot:

   ```bash
   python src/app.py
   ```
# Disclaimer
This project is built strictly for educational purposes and personal portfolio demonstration. It is meant to be run in a safe, controlled, and isolated environment. Do not use this code in production networks without proper security hardening.
