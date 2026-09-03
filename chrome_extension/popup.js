const REQUIRED_KEYS = ["SID", "SAPISID", "HSID", "SSID"];

async function getCookies() {
  const [googleCookies, nlmCookies, nbCookies, nlmUrlCookies, nbUrlCookies] = await Promise.all([
    chrome.cookies.getAll({ domain: "google.com" }),
    chrome.cookies.getAll({ domain: "notebooklm.google.com" }),
    chrome.cookies.getAll({ domain: "notebook.google.com" }),
    chrome.cookies.getAll({ url: "https://notebooklm.google.com/" }),
    chrome.cookies.getAll({ url: "https://notebook.google.com/" })
  ]);

  const map = new Map();
  // 1. First set general google.com cookies
  for (const c of googleCookies) {
    map.set(c.name, c.value);
  }
  // 2. Overwrite with specific notebook cookies (crucial for OSID & __Secure-OSID)
  for (const c of [...nlmCookies, ...nbCookies, ...nlmUrlCookies, ...nbUrlCookies]) {
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
