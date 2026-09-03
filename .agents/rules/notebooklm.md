# NotebookLM Workspace Rule

## Authentication & Token Management

Whenever interacting with the `notebooklm` MCP server in this workspace:

1. **If authentication fails (401 / expired tokens / unauthenticated):**
   - Direct the user to run `python auth_helper.py` in terminal, or execute it if cookies are already placed in `cookies.txt` or clipboard.
   - Provide clear instructions to obtain the `cookie:` header from Chrome/browser DevTools (`F12` -> `Network` -> `batchexecute` -> `cookie:`) if needed.
   - Do not attempt complex manual token extraction scripts; use `auth_helper.py`.

2. **Language Configuration:**
   - Always specify `language: "es"` when triggering Studio creations (`audio_overview_create`, `video_overview_create`, `slide_deck_create`, etc.) unless the user explicitly requests another language.

3. **Workspace Organization:**
   - Keep academic work and deliverables inside `Tareas/`.
   - Keep reference documents and media inside `Recursos/`.
   - Do not litter the workspace root with temporary scratch scripts.
