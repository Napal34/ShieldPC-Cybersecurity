import os
import sys
import time
import psutil
import threading
from datetime import datetime

# Ruta fija para el contenedor Docker (Linux)
HOSTS_PATH = "/etc/hosts"

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
                print(f"\n{obtener_tiempo()} [ALERTA-FIM] El archivo HOSTS ha sido modificado!")
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
                    print(f"{obtener_tiempo()} [MONITOR-PROC] Nuevo proceso detectado -> PID: {proc.pid} | Nombre: {proc.name()}")
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
                        print(f"{obtener_tiempo()} [MONITOR-RED] Conexion establecida externa -> {ip_remota} (PID: {conn.pid})")
        except Exception:
            continue

if __name__ == "__main__":
    print(f"{obtener_tiempo()} [INFO] " + "="*60)
    print(f"{obtener_tiempo()} [INFO]  Desplegando Core Engine Mini-HIDS Avanzado...")
    print(f"{obtener_tiempo()} [INFO] " + "="*60)

    t1 = threading.Thread(target=modulo_fim, daemon=True)
    t2 = threading.Thread(target=modulo_procesos, daemon=True)
    t3 = threading.Thread(target=modulo_red, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    print(f"{obtener_tiempo()} [INFO] Estatus del motor: Monitoreo concurrente activo de forma persistente.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{obtener_tiempo()} [INFO] Apagando el motor de seguridad de forma segura.")
    print(f"{obtener_tiempo()} [INFO] Estatus del motor: Monitoreo concurrente activo de forma persistente.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{obtener_tiempo()} [INFO] Apagando el motor de seguridad de forma segura.")
