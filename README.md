# 🚀 NotebookLM Antigravity MCP Integration

Integración completa entre **Google NotebookLM** y **Google Antigravity IDE** a través del protocolo MCP (Model Context Protocol). Permite consultar cuadernos, investigar fuentes automáticamente con Deep Research, y generar entregables (audios, diapositivas, guías y quizzes) directamente desde el asistente inteligente de Antigravity.

---

## 📁 Estructura del Repositorio

- **`.agents/rules/notebooklm.md`**: Reglas de comportamiento del agente para manejar la autenticación, idiomas y organización.
- **`.agents/skills/using-notebooklm-mcp/SKILL.md`**: Skill estandarizada de Antigravity para interactuar con todas las herramientas de NotebookLM MCP.
- **`chrome_extension/`**: Mini-extensión de Chrome para extraer y sincronizar las cookies de sesión en 1 solo clic.
- **`auth_helper.py`**: Script para validar, guardar y renovar tokens (soporta modo automático con `--auto` leyendo el portapapeles).
- **`notebooklm_mcp_guide.md`**: Guía detallada de instalación y solución de problemas.
- **`.agents/Tutoriales/`**: Transcripciones y prompts maestros para NotebookLM y creación de dashboards.

---

## 🛠️ Prerrequisito: Instalar el Servidor MCP

En tu terminal ejecuta (solo una vez):
```powershell
uv tool install notebooklm-mcp-server
```
*(O `pip install notebooklm-mcp-server` si no tienes uv).*

---

## 🔑 Dos Formas de Conectar tu Sesión (Elige la que prefieras)

Puedes elegir entre el método rápido con la extensión o el método manual sin instalar nada:

### ⚡ Opción 1: Con la Extensión de 1-Clic (Recomendada para uso diario)
Ideal para no tener que abrir la consola de desarrollador cada vez que la sesión caduque:

1. **Instalar la extensión en Chrome (solo la primera vez):**
   - Abre en Chrome: `chrome://extensions`.
   - Activa el interruptor **Modo de desarrollador** (arriba a la derecha).
   - Clic en **Cargar descomprimida** (arriba a la izquierda) y selecciona la carpeta `chrome_extension` de este proyecto.
2. **Uso:**
   - Abre [NotebookLM](https://notebooklm.google.com) con tu cuenta de Google.
   - Haz 1 clic en el icono de la **`N`** (NotebookLM Sync) en tu barra de extensiones (te saldrá un aviso verde de copiado al portapapeles).
   - En Antigravity, dile al asistente:
     > *"Conéctate a NotebookLM"* o *"Has tu magia"*
   - El agente leerá tus credenciales automáticamente y quedará conectado.

---

### 📋 Opción 2: Método Manual desde el Navegador (Sin instalar extensiones)
Ideal si prefieres no instalar ninguna extensión y copiar tus credenciales directamente:

1. Abre tu navegador y entra a [NotebookLM](https://notebooklm.google.com) con tu sesión iniciada.
2. Presiona **`F12`** para abrir las Herramientas de Desarrollador y ve a la pestaña **Network** (Red).
3. Presiona **`F5`** para recargar la página.
4. En la columna de nombres de peticiones, busca y haz clic en **`batchexecute`** (o en cualquier petición que apunte a `google.com`).
5. En el panel de la derecha, ve a la pestaña **Headers** (Encabezados) y baja hasta **Request Headers** (Encabezados de solicitud).
6. Busca la línea que dice **`cookie:`**, selecciona todo su valor y cópialo.
7. **Para conectar:**
   - Pega ese texto directamente aquí en el chat de Antigravity, **o**
   - Pégalo en la terminal ejecutando `python auth_helper.py`.
