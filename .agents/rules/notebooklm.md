# NotebookLM Workspace Rule

## Authentication & Token Management

Whenever interacting with the `notebooklm` MCP server in this workspace:

1. **If authentication fails (401 / expired tokens / RPC Error 16):**
   - **Primary Action (Zero-Prompt):** First check if fresh cookies are in the clipboard by executing:
     ```powershell
     python auth_helper.py --auto
     ```
     If valid cookies are found, call `refresh_auth` and resume seamlessly.
   - **User Guidance:** When explaining how to connect or recover a session, ALWAYS present the two clear options:
     - **Opción 1: Extensión de 1-Clic (Rápida y recomendada):** Instalar `chrome_extension/` en `chrome://extensions` una sola vez. En NotebookLM hacer 1 clic en el icono `N` y decirle al agente *"conéctate"*.
     - **Opción 2: Modo Manual (Sin extensiones):** Entrar a `notebooklm.google.com`, presionar `F12` -> `Network` -> recargar (`F5`) -> clic en `batchexecute` -> copiar el valor del encabezado `cookie:` de Request Headers y pegarlo en el chat o en `python auth_helper.py`.
   - **Never commit credentials:** Cookies and `auth.json` are excluded via `.gitignore`. Never write credentials directly into committed files.

2. **Language Configuration:**
   - Always specify `language: "es"` when triggering Studio creations (`audio_overview_create`, `video_overview_create`, `slide_deck_create`, etc.) unless the user explicitly requests another language.

3. **Workspace Organization:**
   - Keep academic work and deliverables inside `Tareas/`.
   - Keep reference documents and media inside `Recursos/`.
   - Do not litter the workspace root with temporary scratch scripts.
