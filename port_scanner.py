
'''
PORT SCANNER SCRIPT - Documentación:

Este script utiliza Nmap para realizar un escaneo de puertos en un target y exportar los resultados tanto a la consola como a un archivo de texto.
El objetivo es escanear puertos dentro de un rango específico, obtener información sobre los servicios, versiones disponibles y detectar el sistema operativo.
'''

import nmap #nmap module para usar port scans en python / ps : pip install python-nmap

rango_ports = "0-1023" #elegimos el rango de ports que queramos analizar
target = "127.0.0.1" #localhost (NO USES otras IP sin previo PERMISO)

#Inicializador
port_scanner = nmap.PortScanner()
print(f'Escaneando los puertos: {rango_ports} de: {target}...\n')

#Nmap Scan para el rango de puertos + función de detección de servicio (esto es opcional)
#-T4 flag de nmap para + velocidad (también es + AGRESIVO = FÁCILMENTE DETECTABLE)
#para el ejemplo que usaremos (localhost) priorizamos velocidad a detectabilidad
port_scanner.scan(target, rango_ports, arguments="-T4 -sV")


#Abrimos un archivo para ir guardando los resultados obtenidos.
with open("resultados_scanner.txt", "w") as file:

    #Visualización del proceso y resultados
    for port in port_scanner[target]['tcp']: #loop en el rango de puertos dado
        estado = port_scanner[target]['tcp'][port]['state'] #estado del puerto {open,closed,filtered,etc...}
        servicio = port_scanner[target]['tcp'][port].get('name', 'Unknown') #nombre del servicio detectado, .get por si no detecta nada nos muestra 'Unknow' y evitar errores
        version = port_scanner[target]['tcp'][port].get('version', 'N/A') #version del servicio y si no detecta nada evitamos errores mostrando N/A.

        #hacemos un print del resultado para que sea legible al usuario.
        print(f"Puerto {port}: {estado.upper()} | Servicio: {servicio} | Version: {version}")

        file.write(f"Puerto {port}: {estado.upper()} | Servicio: {servicio} | Version: {version}\n")

    if 'osmatch' in port_scanner[target]: #detección de OS (opcional).
        print("\n ¡OS detectado!")
        file.write("\n ¡OS detectado!")
        for os in port_scanner[target]['osmatch']: #loop de coincidencia con OS
            print(f"- {os['name']} ({os['accuracy']}% de precisión)") #visualiza OS detectado y su precisión
            file.write(f"- {os['name']} ({os['accuracy']}% de precisión)")

#Hacemos un print para indicar que los resultados se han exportado correctamente.        
print("\n ¡Escaneo completado!, los resultados se han guardado correctamente en 'resultados_scanner.txt'.")