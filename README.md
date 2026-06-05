import os
import sys
import time
import hashlib
import psutil
from datetime import datetime

PROCESOS_SOSPECHOSOS = ["utorrent", "bittorrent", "wireshark", "mimikatz"]
PUERTOS_PELIGROSOS = [4444, 1337, 9999]
RUTA_ARCHIVO_CRITICO = r"C:\Windows\System32\drivers\etc\hosts" if sys.platform == "win32" else "/etc/hosts"

def obtener_log_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def monitorear_procesos():
    print(f"[{obtener_log_time()}] Analizando procesos activos...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            nombre_proc = proc.info['name'].lower()
            for sospechoso in PROCESOS_SOSPECHOSOS:
                if sospechoso in nombre_proc:
                    print(f"⚠️ ¡ALERTA! Proceso sospechoso: {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def monitorear_red():
    print(f"[{obtener_log_time()}] Escaneando conexiones de red...")
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.raddr:
            ip_remota, puerto_remoto = conn.raddr
            if puerto_remoto in PUERTOS_PELIGROSOS:
                print(f"🚨 ¡ALERTA DE RED! Conexión al puerto {puerto_remoto} en la IP {ip_remota}")

def calcular_hash_archivo(ruta):
    if not os.path.exists(ruta):
        return None
    sha256_hash = hashlib.sha256()
    with open(ruta, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

if __name__ == "__main__":
    print("=" * 60)
    print("  INICIANDO SISTEMA DE CIBERSEGURIDAD BÁSICO (SHIELD-PC)  ")
    print("=" * 60)
    
    hash_inicial = calcular_hash_archivo(RUTA_ARCHIVO_CRITICO)
    print(f"[*] Hash inicial del archivo hosts guardado con éxito.")
    
    try:
        while True:
            monitorear_procesos()
            monitorear_red()
            
            hash_actual = calcular_hash_archivo(RUTA_ARCHIVO_CRITICO)
            if hash_actual != hash_inicial:
                print(f"🔥 ¡ALERTA CRÍTICA! El archivo {RUTA_ARCHIVO_CRITICO} ha sido modificado.")
                hash_inicial = hash_actual 
            
            print(f"[{obtener_log_time()}] Escaneo completado. Esperando 10 segundos...")
            print("-" * 60)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n[+] Apagando el sistema de seguridad de forma segura.")
