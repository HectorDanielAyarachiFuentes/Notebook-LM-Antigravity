# 📘 Guía de Configuración de NotebookLM MCP para Antigravity IDE

Esta guía detalla los prerrequisitos necesarios, los pasos secuenciales para instalar y levantar el servidor MCP de NotebookLM, y un catálogo final de resolución de problemas con los errores más comunes y sus respectivas soluciones.

---

## 🛠️ 1. Requisitos Previos (Prerrequisitos)

Antes de comenzar con la instalación del servidor MCP, asegúrate de tener instalados los siguientes programas en tu sistema operativo:

1.  **Antigravity IDE:** El editor de código inteligente donde conectarás tu agente al servidor MCP.
2.  **Google Chrome o Navegador compatible (como Opera GX):** Necesario para iniciar sesión en NotebookLM y extraer la sesión.
3.  **Python 3.10 o superior:** Requerido para dar soporte a la librería FastMCP y compilar dependencias. Puedes verificarlo en tu terminal ejecutando `python --version`.
4.  **Node.js (versión LTS reciente):** Requerido para la correcta ejecución del protocolo MCP en JavaScript.
5.  **Gestor de paquetes `uv` (o `pip`):** Recomendado para realizar la instalación limpia de las herramientas.

---

## 🚀 2. Pasos para Levantar y Configurar el Servidor

Sigue este orden secuencial para poner en funcionamiento tu servidor MCP:

### Paso A: Instalar el servidor
Abre tu terminal (PowerShell o CMD) y ejecuta el siguiente comando para instalar el servidor globalmente usando `uv`:
```powershell
uv tool install notebooklm-mcp-server
```
*(Si no tienes `uv` instalado, puedes usar `pip install notebooklm-mcp-server`).*

### Paso B: Obtener e Importar las Cookies (Dos Métodos)

Puedes elegir entre el método automático (más directo si cierras el navegador) o el manual (por archivo):

#### 🚀 Opción 1: Modo Automático (Recomendado)
Este método lanza un navegador Chrome temporal controlado por el terminal para capturar las cookies automáticamente:
1. **Cierra completamente todas las ventanas de Google Chrome** en tu sistema.
2. Abre tu terminal y ejecuta:
   ```powershell
   notebooklm-mcp-auth
   ```
3. Se abrirá una ventana de Chrome automáticamente. Si no te redirige solo, navega a `https://notebooklm.google.com` e inicia sesión con tu cuenta de Google.
4. En cuanto entres y el terminal detecte la sesión de cuadernos, guardará los datos automáticamente en `C:\Users\<Usuario>\.notebooklm-mcp\auth.json` y finalizará el comando.

#### 📝 Opción 2: Modo Manual (Por archivo de texto)
Úsala si la versión automática falla, no abre Chrome o da errores de WebSocket.

> 🤖 **Instrucciones para Asistentes de IA (Cómo automatizar este paso):**
> 1. El asistente de IA debe verificar si ya existe el archivo `cookies.txt` en la raíz del espacio de trabajo.
> 2. Si existe, la IA debe ejecutar automáticamente en la terminal del sistema:
>    ```powershell
>    python auth_helper.py
>    ```
>    *Este script detectará automáticamente las cookies de tu portapapeles o de `cookies.txt`, las validará y guardará en la caché de NotebookLM MCP.*
>
> 3. Si el archivo no existe o está vacío, la IA debe dar las siguientes instrucciones claras al usuario para que extraiga la cookie de su navegador habitual, la guarde en `cookies.txt`, o simplemente la copie al portapapeles y ejecute `python auth_helper.py`:
>
> **Pasos para que el usuario obtenga la cookie:**
> 1. Abre tu navegador (Chrome, Opera GX, etc.) y entra a `https://notebooklm.google.com`.
> 2. Presiona **F12** y selecciona la pestaña **Network** (Red).
> 3. Recarga la página (F5) y haz clic en cualquier petición de la lista (por ejemplo, `batchexecute` o `notebooks`).
> 4. En el panel lateral derecho, ve a **Request Headers** y copia todo el valor de la cabecera **`cookie:`** (Clic derecho -> *Copy value*).
> 5. Ejecuta en la terminal `python auth_helper.py` (lo detectará del portapapeles automáticamente) o crea un archivo `cookies.txt` pegando el valor.


### Paso D: Configurar el Editor Antigravity
1. Abre la sección de configuraciones MCP de tu editor (Settings -> MCP Servers -> Manage MCP).
2. Asegúrate de añadir el servidor con la ruta de tu ejecutable. En tu archivo de configuración del editor, la estructura debe verse así:
   ```json
   {
     "mcpServers": {
       "notebooklm": {
         "command": "C:\\Users\\Ramoncito\\.local\\bin\\notebooklm-mcp.exe"
       }
     }
   }
   ```
3. Guarda el archivo de configuración y haz clic en **Refresh** (Actualizar) en la pestaña MCP de tu editor.

---

## 🔍 3. Guía de Errores Comunes y Soluciones

A continuación, se listan los problemas y bloqueos más frecuentes que ocurren al intentar iniciar el servidor, junto con sus causas y soluciones:

| Error / Síntoma | Causa | Solución |
| :--- | :--- | :--- |
| **"Authentication expired"** (a pesar de tener cookies nuevas) | **Incompatibilidad de Dominio:** Google cambió su dominio a `notebook.google.com`. Las cookies pertenecen a ese nuevo dominio, pero la librería tiene hardcodeado el antiguo subdominio `notebooklm.google.com`. | Edita el archivo `api_client.py` en tu librería de Python (`%APPDATA%\uv\tools\notebooklm-mcp-server\Lib\site-packages\notebooklm_mcp\api_client.py`) y cambia la línea 196 a:<br>`BASE_URL = "https://notebook.google.com"` |
| **`WebSocketBadStatusException`** (al autenticar en modo automático) | **Procesos en segundo plano / Aislamiento de GUI:** Hay procesos de Chrome activos en segundo plano que bloquean la conexión, o el terminal de la IA inició Chrome de forma invisible en una sesión aislada. | 1. Cierra todos tus navegadores Chrome activos.<br>2. Ejecuta `taskkill /F /IM chrome.exe` en tu terminal para forzar el cierre.<br>3. Utiliza la autenticación manual por archivo (`--file`) explicada en el Paso B y C. |
| **`Required cookies are missing: ['HSID', 'SSID']`** | **Limitación del Sandbox de Javascript:** Intentaste extraer las cookies inyectando un script (`document.cookie` o `cookieStore`) desde la consola del navegador. Google bloquea el acceso a cookies críticas marcadas como `HttpOnly`. | No utilices scripts ni consolas para extraer las cookies. Copia la cookie directamente desde la sección **Request Headers** en la pestaña **Network** (Red) de las herramientas de desarrollo, tal como se detalla en el Paso B. |
| **`Unknown tool: 'list_notebooks'`** | **Cambio de versión de la herramienta:** El nombre del comando stdio fue actualizado en la última versión de la librería del servidor. | Las herramientas válidas de la versión actual para listar cuadernos son `notebook_list` y `notebook_get`. |
