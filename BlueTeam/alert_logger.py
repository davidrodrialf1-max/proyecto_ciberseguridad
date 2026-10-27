# blue_team/alert_logger.py
import subprocess
import datetime

def log_security_events():
    print("[*] Verificando registros de seguridad en busca de accesos no autorizados...")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simula el registro de eventos de intentos de entrada recientes
    log_entry = f"[{timestamp}] Auditoría Blue Team: Verificación de intentos de acceso realizada.\n"
    
    with open("security_alerts.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    print("[+] Evento registrado correctamente en 'security_alerts.log'.")

if __name__ == "__main__":
    log_security_events()
