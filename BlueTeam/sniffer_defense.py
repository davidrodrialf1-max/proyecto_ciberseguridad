from scapy.all import sniff, ARP
import sys
import datetime
from alert_logger import registrar_alerta

def detect_arp_spoof(packet):
    # Verificamos si el paquete tiene la capa ARP
    if packet.haslayer(ARP):
        # Si detectamos una respuesta ARP (op=2), es un indicio de ARP Spoofing
        if packet[ARP].op == 2:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip_origen = packet[ARP].psrc
            mac_atacante = packet[ARP].hwsrc
            ip_destino = packet[ARP].pdst
            
            # Imprime en consola (como lo tienes ahora)
            print(f"\n Alerta de seguridad [{timestamp}] Tráfico ARP sospechoso detectado.")
            print(f"    -> IP Origen: {ip_origen}")
            print(f"    -> MAC Atacante: {mac_atacante}")
            print(f"    -> IP Destino: {ip_destino}\n")
            
            # <--- ¡FALTA ESTA LÍNEA AQUÍ PARA QUE ESCRIBA EL LOG! --->
            mensaje_log = f"Ataque ARP Spoofing detectado. IP Origen: {ip_origen}, MAC Atacante: {mac_atacante}"
            registrar_alerta("SnifferDefense", mensaje_log)

def start_sniffer():
    print("   BLUE TEAM - IDS / DETECCIÓN DE ARP SPOOFING")
    print(" ")
    print("Iniciando defensa: Sniffer de red activo...")
    print("Monitoreando tráfico en busca de anomalías ARP.")
    print("Presiona Ctrl + C para detener el sniffer.\n")
    
    try:
        # Quitamos el filtro estricto "arp" del motor de Scapy y filtramos por código en Python
        # store=0 evita consumo excesivo de memoria guardando paquetes en RAM
        sniff(prn=detect_arp_spoof, store=0)
    except Exception as e:
        print(f"Error en el sniffer. Asegúrate de ejecutar como Administrador y tener Npcap instalado. Detalle: {e}")

if __name__ == "__main__":
    start_sniffer()
