# blue_team/os_audit.py
import subprocess
import os

def audit_system():
    print("[*] Iniciando auditoría de seguridad del Sistema Operativo (Windows)...")
    
    print("\n--- 1. Verificando estado del Firewall ---")
    subprocess.run("netsh advfirewall show allprofiles state", shell=True)
    
    print("\n--- 2. Listado de usuarios del sistema ---")
    subprocess.run("net user", shell=True)
    
    print("\n--- 3. Conexiones de red activas y puertos escuchando ---")
    subprocess.run("netstat -an | findstr LISTENING", shell=True)

if __name__ == "__main__":
    audit_system()
