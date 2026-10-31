Descripción del propósito del laboratorio.

● Roles de Blue Team y Red Team.

RedTeam: Atacar BlueTeam

BlueTeam: Defender y capturar ataques del RedTeam

● Requisitos (Python, Scapy, Nmap, Azure CLI, etc.).

● Instrucciones de ejecución para cada script.
Metadología de los scripts
1. Escaneo de puertos y srevicios (scanner.py)
   Metodología: Ejecutar escaneos básicos y avanzados a la máquina azul para detectar puertos abiertos y versiones
   
2. Análisis de tráfico y Spoofing (packet_attack.py)
   Metodología: Se utilizó Scapy desde la máquina virtual atacante conectada a la misma red local virtual ZeroTier para realizar pruebas de captura de paquetes y suplantación ARP.
   
4. Pruebas de acceso no autorizado (ssh_brute.py)
   Metodología: Con este script se ejecuta un ataque de diccionario automatizado contra el servicio SSH utilzando credenciales tipo wordlist.
   
● Cómo evaluar el éxito de los ataques o defensas
Mediante la prueba de cada script, así se logra validar si funciona. 
