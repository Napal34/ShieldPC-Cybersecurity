<img width="1892" height="789" alt="image" src="https://github.com/user-attachments/assets/53fb6b24-1f61-4b58-b918-d1251fd412f8" /># 🛡️ Laboratorio de SecOps: Monitoreo de Integridad de Archivos (FIM) con Zabbix y Docker

## 📌 Descripción del Proyecto
Este proyecto de portafolio demuestra la implementación práctica de un sistema **FIM (File Integrity Monitoring)** en un entorno de microservicios contenerizados. El objetivo principal es la auditoría automatizada y la detección temprana de intrusiones en archivos críticos de configuración del sistema operativo Linux (`/etc/passwd`).

El laboratorio simula un entorno real de operaciones de seguridad (**SecOps**), donde cualquier alteración no autorizada en la base de datos de usuarios del servidor gatilla una alerta de alta prioridad en un panel central en menos de 10 segundos.

---

## 🛠️ Stack Tecnológico
* **Plataforma de Observabilidad:** Zabbix Server & Zabbix Agent (v6.4)
* **Infraestructura y Orquestación:** Docker & Docker Compose
* **Entorno de Red Virtual:** Docker Bridge Network (Resolución interna por DNS de contenedores)
* **Sistemas Operativos:** Linux (Contenedores cliente/servidor) / Windows PowerShell (Host)
* **Automatización y Shell:** Bash Linux

---

## 🚀 Arquitectura de la Solución
El entorno se despliega de manera aislada y portable mediante dos nodos principales comunicados internamente:
1. **`Zabbix Server / Web Frontend`:** Centro de control, procesamiento de datos y visualización del SOC.
2. **`servidor-cliente-final`:** Contenedor objetivo que actúa como el servidor de producción auditado, corriendo el servicio nativo de **Zabbix Agent**.

---

## 🔧 Configuración Técnica e Ingeniería de Alertas

### 1. Recolección de Datos (Item de Auditoría)
Se configuró una métrica de control pasivo en el host objetivo utilizando la llave criptográfica nativa del agente:
* **Nombre:** `Monitoreo de Integridad - /etc/passwd`
* **Key:** `vfs.file.cksum[/etc/passwd]` 
* **Función:** Realiza un cálculo automatizado del checksum/hash numérico del archivo objetivo.
* **Intervalo de Muestreo:** `10s` (Optimizado para validación inmediata en laboratorio).

### 2. Lógica del Disparador (Trigger Expresión)
Para automatizar la respuesta ante incidentes sin intervención humana, se programó un disparador basado en álgebra booleana que evalúa la variación de estados:
* **Expresión:** `change(/servidor-cliente-final/vfs.file.cksum[/etc/passwd])=1`
* **Severidad:** **High (Alto)**
* **Explicación:** La función matemática `change()` compara el hash entrante con el inmediatamente anterior. Si el resultado es diferente de cero, la expresión devuelve verdadero (`1`) y levanta la alerta de forma instantánea.

---

## 🥷 Simulación de Ataque y Respuesta ante Incidentes (Validación PoC)

Para validar la resiliencia y efectividad de la sonda de seguridad, se ejecutó una simulación de intrusión forzada saltando los privilegios estándar del agente:

1. **Evasión de restricciones de usuario e ingreso como Superusuario (UID 0):**
   ```bash
   docker exec -u 0 -it servidor-cliente-final bash

----------------------------------------------------------------------------------------------
## 🛡️ Módulo: Orquestación, Filtrado Condicional y Persistencia de Logs (SIEM/Middleware)

Como extensión de las capacidades de monitoreo de **ShieldPC-Cybersecurity**, se implementó un ecosistema contenerizado basado en Docker para la centralización, análisis y filtrado de telemetría de seguridad en tiempo real. Este módulo actúa como un componente *Middleware/SIEM* estratégico para mitigar la fatiga de alertas en la consola de operaciones.

### 🏗️ Arquitectura de la Solución
El entorno opera de manera integrada sobre una infraestructura basada en microservicios:
* **`nodered_windows` (Node-RED):** Motor de orquestación y análisis basado en flujos que recibe eventos crudos vía HTTP POST, procesa los payloads e implementa la lógica de enrutamiento.
* **Zabbix Stack (`zabbix-server`, `zabbix-web`, `zabbix-agent`):** Infraestructura central destinada a la recolección de métricas de salud del sistema, con agentes listos para consumir los registros generados.

### 🔄 Flujo de Trabajo Automatizado
1. **Ingesta (Ingress):** Un script desarrollado en Python (`emisor_alertas.py`) simula un incidente crítico de seguridad (ej: ataque de fuerza bruta en un *Active Directory*) enviando telemetría de red estructurada en formato JSON hacia el endpoint `[post] /alerta`.
2. **Filtrado Condicional (Parsing):** El nodo de función lógica evalúa la propiedad `msg.payload.severidad`:
    * **Gravedad Informativa:** Se desvía directamente a la consola de depuración (`debug 1`) para visualización operativa volátil.
    * **Gravedad Crítica:** Se intercepta, se aísla de la consola general y se direcciona al sistema de archivos para mitigar el ruido visual.
3. **Persistencia e Integración con Zabbix:** Los eventos críticos se escriben de manera págada e irreversible en el volumen del contenedor (`/data/alertas_criticas.log`). Esta persistencia inmutable permite que el **Zabbix Agent** configure un elemento de monitoreo (*Item type: log*) para parsear el archivo, detectar la cadena `"Crítica"` y gatillar disparadores (*Triggers*) de alta prioridad en el Dashboard global de Zabbix.

### 💻 Evidencia de Operación y Validación Forense
Para auditar la persistencia del incidente en el contenedor de infraestructura:

```bash
docker exec -it nodered_windows cat /data/alertas_criticas.log


JSON
{
  "origen": "Servidor-Contabilidad",
  "fecha": "2026-06-22 16:09:13",
  "servicio": "Active-Directory-Windows",
  "mensaje": "CRITICAL: Bloqueo de cuenta Administrador. 15 intentos fallidos desde IP externa sospechosa.",
  "severidad": "Crítica"
}



<img width="861" height="360" alt="image" src="https://github.com/user-attachments/assets/31eecf9d-ee4b-4585-96a3-be349765562e" />







   
