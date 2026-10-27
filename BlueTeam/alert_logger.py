# blue_team/alert_logger.p# blue_team/alert_logger.py
import datetime
import os

LOG_FILE = "security_alerts.log"

def registrar_alerta(origen, mensaje):
    """
    Recibe eventos en tiempo real desde otros scripts (sniffer_defense.py, os_audit.py)
    y los guarda de forma persistente en el archivo de logs.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{origen.upper()}] {mensaje}\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"[LOG GUARDADO] {log_entry.strip()}")
    except Exception as e:
        print(f"[!] Error al escribir en el archivo de logs: {e}")

if __name__ == "__main__":
    print("[*] Módulo Alert Logger listo.")
    print("[*] Este script funciona de forma conectada con los demás módulos de defensa.")
    registrar_alerta("AlertLogger", "Sistema de registro inicializado correctamente.")
