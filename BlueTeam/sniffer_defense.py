# blue_team/sniffer_defense.py
from scapy.all import sniff, ARP
import sys

def detect_arp_spoof(packet):
    # Si detectamos una respuesta ARP (op=2), podría ser un ataque de spoofing
    if packet.haslayer(ARP) and packet[ARP].op == 2:
        print(f"[!] ¡ALERTA DE SEGURIDAD! Tráfico ARP sospechoso detectado de la IP: {packet[ARP].psrc} con MAC: {packet[ARP].hwsrc}")

def start_sniffer():
    print("[*] Iniciando defensa: Sniffer de red activo (Detectando anomalías ARP)...")
    print("[*] Presiona Ctrl + C para detener la defensa y permitir escaneos normales.")
    # Escucha el tráfico de red de forma pasiva
    try:
        sniff(filter="arp", prn=detect_arp_spoof, store=0)
    except Exception as e:
        print(f"[!] Nota: Asegúrate de ejecutar como Administrador y tener Npcap instalado. Error: {e}")

if __name__ == "__main__":
    start_sniffer()
