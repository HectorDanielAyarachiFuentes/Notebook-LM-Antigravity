const REQUIRED_KEYS = ["SID", "SAPISID", "HSID", "SSID"];

async function getCookies() {
  const [googleCookies, nlmCookies] = await Promise.all([
    chrome.cookies.getAll({ domain: "google.com" }),
    chrome.cookies.getAll({ domain: "notebooklm.google.com" })
  ]);

  const map = new Map();
  for (const c of [...googleCookies, ...nlmCookies]) {
    map.set(c.name, c.value);
  }

  const cookiePairs = [];
  for (const [key, value] of map.entries()) {
    cookiePairs.push(`${key}=${value}`);
  }

  return {
    cookieString: cookiePairs.join("; "),
    totalCount: map.size,
    hasRequired: REQUIRED_KEYS.some(k => map.has(k))
  };
}

async function doCopy() {
  const statusEl = document.getElementById("status");
  const countEl = document.getElementById("count");
  const btn = document.getElementById("copyBtn");

  try {
    const { cookieString, totalCount, hasRequired } = await getCookies();

    if (!hasRequired) {
      statusEl.className = "status error";
      statusEl.textContent = "⚠️ No se detectó sesión activa de Google. Abre notebooklm.google.com e inicia sesión primero.";
      return;
    }

    await navigator.clipboard.writeText(cookieString);

    statusEl.className = "status success";
    statusEl.innerHTML = "✅ <b>¡Copiado con éxito!</b><br>Ahora ve a Antigravity y di: <i>'conéctate'</i>";
    countEl.textContent = `${totalCount} cookies extraídas correctamente`;
    btn.innerHTML = "<span>✨</span> ¡Sesión Copiada!";
  } catch (err) {
    statusEl.className = "status error";
    statusEl.textContent = "❌ Error al copiar: " + err.message;
  }
}

document.getElementById("copyBtn").addEventListener("click", doCopy);

// Ejecutar automáticamente al abrir la ventana emergente para máxima rapidez
doCopy();
