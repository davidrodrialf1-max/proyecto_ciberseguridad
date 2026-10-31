# blue_team/firewall_hardening.py
import subprocess
import sys
import socket
import threading
import time

def run_powershell(command):
    """Ejecuta comandos en PowerShell con privilegios del sistema."""
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def configure_windows_firewall():
    """Configura el Firewall para bloquear todo lo entrante y permitir solo 22, 80 y 443."""
    print(" ")
    print("   BLUE TEAM - RESTRICCIÓN Y APERTURA DE PUERTOS")
    print(" ")
    
    # 1. Establecer la política por defecto del Firewall de Windows en Bloquear Entrantes (Block Inbound)
    print(" Configurando política por defecto: Bloquear todo el tráfico entrante...")
    run_powershell("Set-NetFirewallProfile -Profile Domain,Public,Private -DefaultInboundAction Block -DefaultOutboundAction Allow")
    
    # 2. Puertos permitidos según el proyecto (22, 80, 443)
    allowed_ports = [22, 80, 443]
    
    for port in allowed_ports:
        rule_name = f"BlueTeam-Allow-Port-{port}"
        print(f" Creando regla para permitir el puerto {port}...")
        # Comando para permitir explícitamente el puerto de entrada
        cmd = f'New-NetFirewallRule -DisplayName "{rule_name}" -Direction Inbound -LocalPort {port} -Protocol TCP -Action Allow'
        
        success, output = run_powershell(cmd)
        if success:
            print(f"    [+] Puerto {port} abierto con éxito en el Firewall.")
        else:
            if "ya existe" in output.lower() or "already exists" in output.lower():
                print(f"    [i] La regla para el puerto {port} ya se encontraba registrada.")
            else:
                print(f"    [!] Nota en regla {port}: {output}")

def start_dummy_listener(port):
    """Mantiene un servicio activo escuchando en el puerto para que Nmap lo detecte 'open'."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", port))
        server.listen(5)
        print(f"    [+] Servicio simulado escuchando en el puerto {port}.")
        
        while True:
            client, addr = server.accept()
            client.close()
    except Exception as e:
        print(f"    [!] No se pudo iniciar el servicio en el puerto {port}: {e}")

if __name__ == "__main__":
    print("[!] Asegúrate de ejecutar este script en PowerShell COMO ADMINISTRADOR.\n")
    
    # 1. Aplicar las reglas del firewall (Cierra todo y solo abre 22, 80, 443)
    configure_windows_firewall()
    
    print(" ")
    print("   INICIANDO SERVICIOS EN LOS PUERTOS PERMITIDOS")
    print(" ")
    
    # 2. Levantar los servicios en los puertos permitidos para la prueba con Nmap
    ports_to_simulate = [22, 80, 443]
    
    for port in ports_to_simulate:
        listener_thread = threading.Thread(target=start_dummy_listener, args=(port,), daemon=True)
        listener_thread.start()

    print("\n[+] Configuración aplicada correctamente.")
    print("[*] Todos los demás puertos están bloqueados por el Firewall.")
    print("[*] Presiona CTRL + C cuando desees detener el script.\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Deteniendo el script y cerrando los servicios.")
