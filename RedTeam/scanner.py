# red_team/scanner.py
import subprocess
import sys

# Ruta exacta del ejecutable de Nmap en Windows
NMAP_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"

def execute_scan(target_ip, flags_list):
    """Ejecuta el comando Nmap combinando la ruta, las banderas y la IP objetivo."""
    comando = [NMAP_PATH] + flags_list + [target_ip]
    
    print(f"\n[*] Ejecutando: {' '.join(comando)}")
    print("[*] Espere un momento mientras se completa el escaneo...\n")
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        print(" RESULTADOS DEL ESCANEO ")
        print(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f" Error durante la ejecución de Nmap: {e}")
        if e.stderr:
            print(f" Detalle del error: {e.stderr}")
    except FileNotFoundError:
        print(f" No se encontró el ejecutable de Nmap en la ruta: {NMAP_PATH}")
        print(" Verifique que Nmap esté instalado correctamente en esa ubicación.")

def show_menu(target_ip):
    """Despliega el menú interactivo de opciones de escaneo."""
    while True:
        print(" ")
        print("Escaneo con nmap")
        print(f"Objetivo actual: {target_ip}")
        print(" ")
        print("1. Colocar el comando propio que desee")
        print("2. Ejecutarle un escaneo básico (-sS)")
        print("3. Ejecutarle un escaneo avanzado (-A -sV -T1 -Pn)")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            custom_flags = input("Ingrese las banderas/parámetros para Nmap (ej. -p 80,22 -sV): ").strip()
            # Dividir la cadena de banderas ingresada en una lista
            flags_list = custom_flags.split() if custom_flags else []
            execute_scan(target_ip, flags_list)
            
        elif opcion == "2":
            print("\n Selección: Escaneo Básico TCP SYN (-sS)")
            execute_scan(target_ip, ["-sS"])
            
        elif opcion == "3":
            print("\n Selección: Escaneo Avanzado (-A -sV -Pn)")
            execute_scan(target_ip, ["-A", "-Pn"])
            
        elif opcion == "4":
            print(" ")
            print("Saliendo")
            break
        else:
            print("\n Opción no válida. Por favor, ingrese un número del 1 al 4.")

if __name__ == "__main__":
    print("Iniciando el script")
    
    # Obtener IP desde argumento de consola o solicitarla al inicio
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("Ingrese la IP objetivo: ").strip()
    
    if target:
        show_menu(target)
    else:
        print("[!] No se ingresó ninguna IP objetivo. Cerrando el script.")
