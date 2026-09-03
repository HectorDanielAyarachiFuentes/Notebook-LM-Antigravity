# 🚀 NotebookLM Antigravity MCP Integration

Integración completa entre **Google NotebookLM** y **Google Antigravity IDE** a través del protocolo MCP (Model Context Protocol). Permite consultar cuadernos, investigar fuentes automáticamente con Deep Research, y generar entregables (audios, diapositivas, guías y quizzes) directamente desde el asistente inteligente de Antigravity.

---

## 📁 Estructura del Repositorio

- **`.agents/rules/notebooklm.md`**: Reglas globales de comportamiento del agente para manejar la autenticación, idiomas y organización.
- **`.agents/skills/using-notebooklm-mcp/SKILL.md`**: Skill estandarizada de Antigravity para interactuar con todas las herramientas de NotebookLM MCP.
- **`chrome_extension/`**: Mini-extensión de Chrome para extraer y sincronizar las cookies de sesión en 1 solo clic.
- **`auth_helper.py`**: Script de soporte para validar, guardar y renovar tokens (soporta modo automático con `--auto` leyendo el portapapeles).
- **`notebooklm_mcp_guide.md`**: Guía detallada paso a paso de instalación y solución de problemas.
- **`.agents/Tutoriales/`**: Transcripciones y prompts maestros para NotebookLM y creación de dashboards.

---

## ⚡ Cómo Proceder (Guía para Cualquier Usuario)

### Paso 1: Configurar el Servidor MCP
Asegúrate de tener instalado el servidor MCP en tu sistema:
```powershell
uv tool install notebooklm-mcp-server
```
*(O `pip install notebooklm-mcp-server` si no usas uv)*.

### Paso 2: Activar la Extensión de 1-Clic en Chrome
Para evitar abrir DevTools (`F12`) cada vez que la sesión caduque:
1. Abre en Chrome: `chrome://extensions`.
2. Activa el interruptor **Modo de desarrollador** (arriba a la derecha).
3. Haz clic en **Cargar descomprimida** (arriba a la izquierda).
4. Selecciona la carpeta `chrome_extension` de este repositorio.

### Paso 3: Conectar y Usar
1. Inicia sesión en [NotebookLM](https://notebooklm.google.com).
2. Haz clic en el icono de la extensión **NotebookLM Sync** en tu barra de extensiones de Chrome (copiará tus cookies al portapapeles).
3. En Antigravity, dile al agente:
   > *"Conéctate a NotebookLM"* o *"Actualiza sesión"*
4. El agente leerá automáticamente tus credenciales y quedará 100% conectado.

---

## 🛠️ Métodos Alternativos de Autenticación

Si no utilizas la extensión de Chrome, puedes usar cualquiera de estos métodos:
- **Método Manual por DevTools:** Entra a `notebooklm.google.com` -> `F12` -> pestaña `Network` -> recarga (`F5`) -> haz clic en `batchexecute` -> copia el valor del encabezado `cookie:` y pégalo en el chat o en `cookies.txt`.
- **Método CLI:** Cierra Chrome y ejecuta en terminal:
  ```powershell
  notebooklm-mcp-auth
  ```
