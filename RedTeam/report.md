Objetivo del ataque.
Evaluar la seguridad de la máquina azul en un entorno controlado de Microsoft Azure

Metadología de los scripts
1. Escaneo de puertos y srevicios (scanner.py)
   Metodología: Ejecutar escaneos básicos y avanzados a la máquina azul para detectar puertos abiertos y versiones
   
   Evidencias y hallazgos:
   
   1.1 Se idenficaron los puertos abiertos principales:
   
   2.2 Servicios de los puertos:
   
2. Análisis de tráfico y Spoofing (packet_attack.py)

   Metodología: Se utilizó Scapy desde la máquina virtual atacante conectada a la misma red local virtual ZeroTier para realizar pruebas de captura de paquetes y suplantación ARP.
   
   Evidencias y hallazgos:
   
   1.1 El script funciona perfecto, lanza ARP e imprime todo el trafico de red del la Blue
   
4. Pruebas de acceso no autorizado (ssh_brute.py)

   Metodología: Con este script se ejecuta un ataque de diccionario automatizado contra el servicio SSH utilzando credenciales tipo wordlist.
   
   Evidencias y hallazgos:
   
   1.1 Se logró identificar la contraseña que utiliza el Windows de la máquina Azul.
   
5. Conclusiones y recomendaciones

   Restringir el acceso mediante SSH
   
   Bloquear de manera automatizada altos volúmenes de ARP 
   
