# 🚀 NotebookLM Antigravity MCP Setup

Este directorio contiene los archivos y la configuración necesarios para integrar **Google NotebookLM** dentro de **Antigravity IDE** a través del protocolo MCP (Model Context Protocol).

---

## 📁 Estructura del Proyecto

- **`.agents/skills/using-notebooklm-mcp/SKILL.md`**: Instrucciones estructuradas para que los agentes inteligentes de Antigravity sepan cómo interactuar de forma consistente con las herramientas del MCP.
- **`cookies.txt`**: Archivo temporal utilizado para importar tus credenciales y cookies de sesión del navegador.
- **`mcp_settings_backup.json`**: Una copia de respaldo de la configuración que agregamos a tu editor.

---

## ⚙️ ¿Dónde están las configuraciones reales?

Para que funcionen globalmente y a nivel de editor, los archivos se instalan en estas ubicaciones del sistema:

1. **Credenciales (`auth.json`)**: 
   Guardado en `C:\Users\Ramoncito\.notebooklm-mcp\auth.json`. Este archivo guarda tus tokens de sesión validados y es el que lee el servidor.
   
2. **Configuración del Editor (`cline_mcp_settings.json`)**:
   Ubicado en el almacenamiento global de Antigravity IDE:
   `c:\Users\Ramoncito\AppData\Roaming\Antigravity IDE\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   Esto le indica al editor que levante automáticamente el servidor MCP.

---

## 🛠️ Re-autenticación (Si tu sesión expira)

Si en el futuro recibes un error diciendo que tu sesión ha expirado:
1. Abre tu terminal habitual (PowerShell o CMD).
2. Ejecuta:
   ```powershell
   notebooklm-mcp-auth
   ```
3. Se abrirá una ventana de Chrome para que inicies sesión en Google, y el terminal guardará las cookies automáticamente.
