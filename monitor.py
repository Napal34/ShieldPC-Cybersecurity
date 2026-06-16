import os
import sys
import time
import psutil
import threading
import socket
import json
import struct
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE TU ZABBIX LOCAL
# ==========================================
ZABBIX_SERVER = "127.0.0.1"  
ZABBIX_PORT = 10051
ZABBIX_HOST = "CyberShield-HIDS"  # Coincide con el Host que creamos en tu Zabbix
HOSTS_PATH = "/etc/hosts"

def enviar_a_zabbix(key, valor):
    """Envía la alerta al puerto 10051 de Zabbix usando sockets puros"""
    try:
        datos = {
            "request": "sender data",
            "data": [
                {
                    "host": ZABBIX_HOST,
                    "key": key,
                    "value": valor
                }
            ]
        }
        json_payload = json.dumps(datos).encode('utf-8')
        
        # Construcción del Header obligatorio de Zabbix (ZBXD\x01 + longitud en 64-bit)
        header = b'ZBXD\x01' + struct.pack('<Q', len(json_payload))
        packet = header + json_payload

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((ZABBIX_SERVER, ZABBIX_PORT))
            s.sendall(packet)
            respuesta = s.recv(1024)
            # Muestra en la consola de VS Code si Zabbix procesó el paquete
            print(f"{obtener_tiempo()} [ZABBIX-LINK] Respuesta del servidor: {respuesta[13:].decode('utf-8')}")
    except Exception as e:
        print(f"{obtener_tiempo()} [ZABBIX-ERROR] No se pudo enviar telemetría: {e}")

def obtener_tiempo():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def modulo_fim():
    print(f"{obtener_tiempo()} [INFO] Sub-modulo inicializado con exito: [Modulo-FIM]")
    try:
        time.sleep(1)
        ultima_modif = os.path.getmtime(HOSTS_PATH)
        while True:
            time.sleep(2)
            actual_modif = os.path.getmtime(HOSTS_PATH)
            if actual_modif != ultima_modif:
                msg_alerta = "¡Alerta de Seguridad! El archivo HOSTS fue modificado."
                print(f"\n{obtener_tiempo()} [ALERTA-FIM] {msg_alerta}")
                
                # ENVIAMOS LA ALERTA A TU DASHBOARD EN VIVO
                enviar_a_zabbix("hids.fim.alert", msg_alerta)
                
                ultima_modif = actual_modif
    except Exception as e:
        print(f"{obtener_tiempo()} [ERROR-FIM] No se pudo acceder a {HOSTS_PATH}: {e}")

def modulo_procesos():
    print(f"{obtener_tiempo()} [INFO] Sub-modulo inicializado con exito: [Modulo-Procesos]")
    procesos_conocidos = set(p.pid for p in psutil.process_iter())
    while True:
        time.sleep(3)
        for proc in psutil.process_iter():
            try:
                if proc.pid not in procesos_conocidos:
                    procesos_conocidos.add(proc.pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

def modulo_red():
    print(f"{obtener_tiempo()} [INFO] Sub-modulo inicializado con exito: [Modulo-Red]")
    conexiones_vistas = set()
    while True:
        time.sleep(4)
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    ip_remota = f"{conn.raddr.ip}:{conn.raddr.port}"
                    if ip_remota not in conexiones_vistas:
                        conexiones_vistas.add(ip_remota)
        except Exception:
            continue

if __name__ == "__main__":
    print(f"{obtener_tiempo()} [INFO] " + "="*60)
    print(f"{obtener_tiempo()} [INFO]  Desplegando Core Engine HIDS + Zabbix Link...")
    print(f"{obtener_tiempo()} [INFO] " + "="*60)

    t1 = threading.Thread(target=modulo_fim, daemon=True)
    t2 = threading.Thread(target=modulo_procesos, daemon=True)
    t3 = threading.Thread(target=modulo_red, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    print(f"{obtener_tiempo()} [INFO] Estatus del motor: Monitoreo concurrente activo conectado a Zabbix.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{obtener_tiempo()} [INFO] Apagando el motor de seguridad de forma segura.")
