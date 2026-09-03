"""
NotebookLM Auth Helper
Herramienta CLI para configurar y actualizar las cookies de autenticación de NotebookLM MCP
de forma automática (portapapeles o cookies.txt) o manual (pegado en terminal).
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Añadir el entorno uv de notebooklm-mcp si está disponible para reutilizar sus librerías
site_packages = r"C:\Users\Ramoncito\AppData\Roaming\uv\tools\notebooklm-mcp-server\Lib\site-packages"
if os.path.exists(site_packages) and site_packages not in sys.path:
    sys.path.insert(0, site_packages)

REQUIRED_COOKIES = ["SID", "HSID", "SSID", "APISID", "SAPISID"]


def get_cache_path() -> Path:
    """Ruta donde NotebookLM MCP almacena los tokens de autenticación."""
    cache_dir = Path.home() / ".notebooklm-mcp"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / "auth.json"


def get_clipboard_text() -> str:
    """Obtiene el contenido del portapapeles usando PowerShell (nativo en Windows)."""
    try:
        cmd = ["powershell", "-NoProfile", "-Command", "Get-Clipboard"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        return result.stdout.strip()
    except Exception:
        return ""


def parse_cookie_string(raw: str) -> dict[str, str]:
    """Extrae las cookies en un diccionario clave-valor."""
    cookies = {}
    if not raw:
        return cookies

    # Limpiar posibles prefijos como 'cookie:' o 'Cookie:'
    cleaned = raw.strip()
    if cleaned.lower().startswith("cookie:"):
        cleaned = cleaned[7:].strip()

    for item in cleaned.split(";"):
        item = item.strip()
        if "=" in item:
            key, val = item.split("=", 1)
            cookies[key.strip()] = val.strip()
    return cookies


def is_valid_google_cookies(cookies: dict[str, str]) -> bool:
    """Verifica si contiene las cookies mínimas requeridas de Google."""
    matches = sum(1 for req in REQUIRED_COOKIES if req in cookies)
    # Si tiene al menos SID y SAPISID o la mayoría de los requeridos
    return matches >= 2 and ("SID" in cookies or "SAPISID" in cookies or "__Secure-1PAPISID" in cookies)


def save_tokens(cookies: dict[str, str], csrf_token: str = "", session_id: str = "") -> Path:
    """Guarda las cookies en el formato JSON esperado por NotebookLM MCP."""
    cache_file = get_cache_path()
    payload = {
        "cookies": cookies,
        "csrf_token": csrf_token,
        "session_id": session_id,
        "extracted_at": time.time(),
    }
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return cache_file


def test_authentication(cookies: dict[str, str]) -> tuple[bool, str]:
    """Prueba si las credenciales funcionan llamando a NotebookLMClient."""
    try:
        from notebooklm_mcp.api_client import NotebookLMClient

        client = NotebookLMClient(cookies=cookies)
        notebooks = client.list_notebooks()
        return True, f"Conexión exitosa. Se encontraron {len(notebooks)} cuadernos en tu cuenta."
    except Exception as e:
        return False, str(e)


def main():
    print("\n" + "=" * 60)
    print(" 🚀 NotebookLM MCP - Asistente de Autenticación Rápida")
    print("=" * 60 + "\n")

    raw_cookies = ""
    source_found = ""

    # 1. Intentar leer desde cookies.txt en el directorio actual
    txt_path = Path("cookies.txt")
    if txt_path.exists():
        try:
            content = txt_path.read_text(encoding="utf-8", errors="ignore").strip()
            parsed = parse_cookie_string(content)
            if is_valid_google_cookies(parsed):
                raw_cookies = content
                source_found = "archivo 'cookies.txt'"
        except Exception:
            pass

    # 2. Intentar leer desde el portapapeles si no se encontró en archivo
    if not raw_cookies:
        clip_content = get_clipboard_text()
        parsed_clip = parse_cookie_string(clip_content)
        if is_valid_google_cookies(parsed_clip):
            raw_cookies = clip_content
            source_found = "el portapapeles de Windows"

    is_auto = "--auto" in sys.argv or "--clipboard" in sys.argv

    # Si se detectó automáticamente
    if raw_cookies:
        parsed = parse_cookie_string(raw_cookies)
        print(f"✨ ¡Cookies de Google detectadas automáticamente desde {source_found}!")
        print(f"   - Total de cookies encontradas: {len(parsed)}")
        present_keys = [k for k in REQUIRED_COOKIES if k in parsed]
        print(f"   - Claves esenciales encontradas: {', '.join(present_keys)}")
        print()
        if is_auto:
            cookies_to_save = parsed
        else:
            choice = input("¿Deseas guardar y probar estas credenciales? [S/n]: ").strip().lower()
            if choice in ("", "s", "si", "y", "yes"):
                cookies_to_save = parsed
            else:
                raw_cookies = ""
    elif is_auto:
        print("❌ Error: No se encontraron cookies válidas en el portapapeles ni en cookies.txt.")
        sys.exit(1)

    # 3. Modo Manual (si no se detectó o el usuario prefirió ingresar manualmente)
    if not raw_cookies and not is_auto:
        print("\n📋 Modo Manual:")
        print("1. En tu navegador abre https://notebooklm.google.com con tu sesión iniciada.")
        print("2. Abre DevTools (F12) -> pestaña Network (Red) -> Recarga (F5).")
        print("3. Clic en una petición (ej. 'batchexecute') -> Request Headers -> Copia el valor de 'cookie:'.\n")
        
        user_input = input("👉 Pega el valor de la cookie aquí y presiona Enter:\n> ").strip()
        cookies_to_save = parse_cookie_string(user_input)

        if not cookies_to_save:
            print("\n❌ Error: No se ingresaron cookies válidas.")
            sys.exit(1)

        if not is_valid_google_cookies(cookies_to_save):
            print("\n⚠️ Advertencia: No se encontraron todas las cookies esenciales (SID, SAPISID, etc.).")
            proceed = input("¿Deseas continuar de todos modos? [s/N]: ").strip().lower()
            if proceed not in ("s", "si", "y", "yes"):
                sys.exit(1)

    # 4. Guardar credenciales
    cache_path = save_tokens(cookies_to_save)
    print(f"\n💾 Credenciales guardadas correctamente en:\n   {cache_path}")

    # 5. Probar autenticación
    print("\n🔍 Verificando acceso con los servidores de NotebookLM...")
    ok, msg = test_authentication(cookies_to_save)
    if ok:
        print(f"\n✅ {msg}")
        print("🎉 ¡NotebookLM MCP está 100% configurado y listo para usarse!")
    else:
        print(f"\n⚠️ Guardado, pero la prueba de conexión reportó: {msg}")
        print("   Nota: Si acabas de iniciar sesión, puede que el servidor tarde unos segundos en sincronizar.")


if __name__ == "__main__":
    main()
