# blue_team/firewall_hardening.py
import subprocess
import sys

def apply_hardening():
    print("==================================================")
    print("     BLUE TEAM - FIREWALL HARDENING (IPTABLES)")
    print("==================================================")
    
    # Lista de comandos de iptables para aplicar el endurecimiento y las reglas de seguridad
    commands = [
        # 1. Limpiar reglas anteriores
        "iptables -F",
        "iptables -X",
        
        # 2. Establecer políticas por defecto (Denegar entrantes, permitir salientes)
        "iptables -P INPUT DROP",
        "iptables -P FORWARD DROP",
        "iptables -P OUTPUT ACCEPT",
        
        # 3. Permitir loopback y conexiones establecidas
        "iptables -A INPUT -i lo -j ACCEPT",
        "iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
        
        # 4. Permitir puertos necesarios (22 SSH, 80 HTTP, 443 HTTPS)
        "iptables -A INPUT -p tcp --dport 22 -j ACCEPT",
        "iptables -A INPUT -p tcp --dport 80 -j ACCEPT",
        "iptables -A INPUT -p tcp --dport 443 -j ACCEPT",
        
        # 5. Rate-Limiting para SSH (Prevención de Fuerza Bruta)
        "iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set",
        "iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP",
        "iptables -A INPUT -p tcp --dport 22 -j ACCEPT",
        
        # 6. Reglas defensivas contra escaneos maliciosos (XMAS, NULL)
        "iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP",
        "iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP",
        "iptables -A INPUT -p tcp --tcp-flags ALL SYN,FIN -j DROP",
        
        # 7. Habilitar registro (Logging) de paquetes bloqueados
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

    print("\n[+] Hardening de Firewall completado exitosamente.")

if __name__ == "__main__":
    apply_hardening()
