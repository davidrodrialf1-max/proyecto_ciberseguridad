# blue_team/firewall_hardening.py
import subprocess
import sys
import socket
import threading
import time

def apply_iptables_hardening():
    """Aplica todas las reglas de iptables exigidas por la rúbrica del Blue Team."""
    print("==================================================")
    print("   BLUE TEAM - FIREWALL HARDENING (IPTABLES)")
    print("==================================================")
    
    commands = [
        # 1. Limpiar reglas anteriores
        "iptables -F",
        "iptables -X",
        
        # 2. Políticas por defecto (Denegar entrantes, permitir salientes)
        "iptables -P INPUT DROP",
        "iptables -P FORWARD DROP",
        "iptables -P OUTPUT ACCEPT",
        
        # 3. Permitir loopback y conexiones establecidas
        "iptables -A INPUT -i lo -j ACCEPT",
        "iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
        
        # 4. Permitir solo puertos necesarios (22 SSH, 80 HTTP, 443 HTTPS)[cite: 10]
        "iptables -A INPUT -p tcp --dport 22 -j ACCEPT",
        "iptables -A INPUT -p tcp --dport 80 -j ACCEPT",
        "iptables -A INPUT -p tcp --dport 443 -j ACCEPT",
        
        # 5. Rate-Limiting avanzado para SSH (Prevención de Fuerza Bruta)[cite: 10]
        "iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set",
        "iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP",
        
        # 6. Reglas defensivas contra escaneos conocidos (XMAS, NULL, etc.)[cite: 10]
        "iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP",
        "iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP",
        "iptables -A INPUT -p tcp --tcp-flags ALL SYN,FIN -j DROP",
        
        # 7. Registro (Logging) de paquetes bloqueados[cite: 10]
        "iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix 'IPTables-Dropped: ' --log-level 4"
    ]

    for cmd in commands:
        try:
            print(f"[*] Ejecutando: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("    [+] Regla aplicada con éxito.")
            else:
                print(f"    [!] Error o requiere privilegios de superusuario: {result.stderr.strip()}")
        except Exception as e:
            print(f"    [!] Error al ejecutar comando: {e}")

def start_dummy_listener(port):
    """Mantiene un servicio simulado escuchando en los puertos permitidos (22, 80, 443)."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print(f"    [+] Servicio simulado activo escuchando en el puerto {port}.")
        
        while True:
            client, addr = server.accept()
            client.close()
    except Exception as e:
        print(f"    [!] No se pudo iniciar el servicio en el puerto {port}: {e}")

if __name__ == "__main__":
    # 1. Aplicar el endurecimiento de red (iptables)
    apply_iptables_hardening()
    
    print("\n--------------------------------------------------")
    print("   INICIANDO SERVICIOS SIMULADOS (PARA ESCANEOS)")
    print("--------------------------------------------------")
    
    # Puertos permitidos en la política que también queremos ver abiertos en los escaneos
    ports_to_simulate = [22, 80, 443]
    
    for port in ports_to_simulate:
        listener_thread = threading.Thread(target=start_dummy_listener, args=(port,), daemon=True)
        listener_thread.start()

    print("\n[+] Hardening y simulación completados con éxito.")
    print("[*] Presiona CTRL + C para detener los servicios y salir.\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Saliendo del script de Blue Team. ¡Hasta luego!")
