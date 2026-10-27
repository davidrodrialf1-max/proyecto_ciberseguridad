# blue_team/sniffer_defense.py
from scapy.all import sniff, ARP
import sys
import datetime
from alert_logger import registrar_alerta

def detect_arp_spoof(packet):
    # Verificamos si el paquete tiene la capa ARP
    if packet.haslayer(ARP):
        # Opcional: Imprimir todos los paquetes ARP que ve (para depurar y ver que sí está leyendo tráfico)
        # print(f"[DEBUG] Paquete ARP detectado: OP={packet[ARP].op} | IP={packet[ARP].psrc} | MAC={packet[ARP].hwsrc}")
        
        # Si detectamos una respuesta ARP (op=2), es un indicio de ARP Spoofing
        if packet[ARP].op == 2:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[!] ¡ALERTA DE SEGURIDAD! [{timestamp}] Tráfico ARP sospechoso detectado.")
            print(f"    -> IP Origen: {packet[ARP].psrc}")
            print(f"    -> MAC Atacante: {packet[ARP].hwsrc}")
            print(f"    -> IP Destino: {packet[ARP].pdst}\n")

def start_sniffer():
    print("==================================================")
    print("   BLUE TEAM - IDS / DETECCIÓN DE ARP SPOOFING")
    print("==================================================")
    print("[*] Iniciando defensa: Sniffer de red activo...")
    print("[*] Monitoreando tráfico en busca de anomalías ARP.")
    print("[*] Presiona Ctrl + C para detener el sniffer.\n")
    
    try:
        # Quitamos el filtro estricto "arp" del motor de Scapy y filtramos por código en Python
        # store=0 evita consumo excesivo de memoria guardando paquetes en RAM
        sniff(prn=detect_arp_spoof, store=0)
    except Exception as e:
        print(f"[!] Error en el sniffer. Asegúrate de ejecutar como Administrador y tener Npcap instalado. Detalle: {e}")

if __name__ == "__main__":
    start_sniffer()
