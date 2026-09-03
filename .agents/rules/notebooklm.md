# NotebookLM Workspace Rule

## Authentication & Token Management

Whenever interacting with the `notebooklm` MCP server in this workspace:

1. **If authentication fails (401 / expired tokens / RPC Error 16):**
   - **Primary Action (Zero-Prompt):** First check if fresh cookies are in the clipboard by executing:
     ```powershell
     python auth_helper.py --auto
     ```
     If valid cookies are found, call `refresh_auth` and resume seamlessly.
   - **User Guidance:** If auto-renewal fails, guide the user with the easiest method:
     - **Option 1 (Fastest / 1-Click):** If the user has loaded `chrome_extension/` in Chrome, tell them to simply click the extension icon on NotebookLM, which copies the session to the clipboard, and then say *"conéctate"*.
     - **Option 2 (Manual DevTools):** Go to `notebooklm.google.com` -> `F12` -> `Network` -> `F5` -> click `batchexecute` -> copy `cookie:` value and paste it or run `python auth_helper.py`.
     - **Option 3 (CLI Auto):** Close Chrome and run `notebooklm-mcp-auth` in terminal.
   - **Never commit credentials:** Cookies and `auth.json` are excluded via `.gitignore`. Never write credentials directly into committed files.

2. **Language Configuration:**
   - Always specify `language: "es"` when triggering Studio creations (`audio_overview_create`, `video_overview_create`, `slide_deck_create`, etc.) unless the user explicitly requests another language.

3. **Workspace Organization:**
   - Keep academic work and deliverables inside `Tareas/`.
   - Keep reference documents and media inside `Recursos/`.
   - Do not litter the workspace root with temporary scratch scripts.
