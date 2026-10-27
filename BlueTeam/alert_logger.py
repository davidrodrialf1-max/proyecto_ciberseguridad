# blue_team/alert_logger.p# blue_team/alert_logger.py
# blue_team/alert_logger.py
import datetime
import time

LOG_FILE = "security_alerts.log"

def registrar_alerta(origen, mensaje):
    """
    Función para que otros scripts (como sniffer_defense.py) 
    envíen alertas y se escriban de forma persistente.
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
    print("==================================================")
    print("   BLUE TEAM - GESTOR Y REGISTRO DE ALERTAS")
    print("==================================================")
    print("[*] Alert Logger activo y en ejecución continua.")
    print("[*] Presiona CTRL + C para detener el servicio de logs.\n")
    
    # Registrar evento de inicio
    registrar_alerta("AlertLogger", "Servicio de alertas iniciado y en espera de eventos.")
    
    try:
        # Bucle infinito para mantener el script abierto en segundo plano
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Servicio de alertas detenido correctamente por el usuario. ¡Hasta luego!")
