from scapy.all import sniff, TCP, IP
import sys
import datetime
from alert_logger import registrar_alerta

def detect_ssh_brute_force(packet):
    
    if packet.haslayer(TCP) and packet.haslayer(IP):
        
        if packet[TCP].dport == 22 or packet[TCP].sport == 22:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip_origen = packet[IP].src
            ip_destino = packet[IP].dst
            puerto_origen = packet[TCP].sport
            
            # Imprime en consola con un formato de alerta similar
            print(f"\n[!] Alerta de seguridad [{timestamp}] Actividad SSH sospechosa / Fuerza Bruta detectada.")
            print(f"    -> IP Origen (Atacante): {ip_origen}")
            print(f"    -> IP Destino (Víctima): {ip_destino}")
            print(f"    -> Puerto TCP: {packet[TCP].dport}\n")
            
            
            mensaje_log = f"Intento de acceso SSH detectado desde la IP: {ip_origen} hacia el puerto 22"
            registrar_alerta("BlueTeam-SSH-Defense", mensaje_log)

def start_sniffer():
    print("   BLUE TEAM - IDS / DETECCIÓN DE ACCESOS SSH EN AZURE")
    print(" ")
    print("Iniciando defensa: Sniffer de red activo en puerto 22...")
    print("Monitoreando tráfico TCP/IP en busca de ataques de fuerza bruta.")
    print("Presiona Ctrl + C para detener el sniffer.\n")
    
    try:
        
        sniff(filter="tcp port 22", prn=detect_ssh_brute_force, store=0)
    except Exception as e:
        print(f"Error en el sniffer. Asegúrate de ejecutar como Administrador y tener Npcap instalado. Detalle: {e}")

if __name__ == "__main__":
    start_sniffer()
