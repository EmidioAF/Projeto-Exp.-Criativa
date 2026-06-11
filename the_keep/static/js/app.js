/* app.js — JavaScript principal do The Keep */

// ---------- Tema claro/escuro ----------
const html = document.documentElement;
const themeBtn = document.getElementById('theme-toggle');
const saved = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', saved);
themeBtn && (themeBtn.textContent = saved === 'dark' ? '☀' : '☾');

themeBtn && themeBtn.addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  themeBtn.textContent = next === 'dark' ? '☀' : '☾';
});

// ---------- Logout automático por inatividade (500 segundos) ----------
(function () {
  const TIMEOUT_MS = 500 * 1000;  // 500 segundos
  const AVISO_MS   = 300 * 1000;  // aviso 300 segundos antes

  if (!window.USUARIO_LOGADO) return;

  let timerLogout, timerAviso;
  let avisoEl = null;

  function criarAviso() {
    if (avisoEl) return;
    avisoEl = document.createElement('div');
    avisoEl.id = 'inatividade-aviso';
    avisoEl.innerHTML = `
      <span>⚠ Você será deslogado em <strong id="inatividade-contador">3</strong>s por inatividade.</span>
      <button onclick="resetInatividade()">Continuar</button>
    `;
    Object.assign(avisoEl.style, {
      position: 'fixed', bottom: '1.5rem', right: '1.5rem',
      background: '#1a3a5c', border: '1px solid #2d7dd2',
      color: '#dce8f5', padding: '1rem 1.4rem', borderRadius: '8px',
      zIndex: '9999', display: 'flex', gap: '1rem', alignItems: 'center',
      boxShadow: '0 4px 20px rgba(0,0,0,0.5)', fontFamily: 'sans-serif',
      fontSize: '0.95rem',
    });
    document.body.appendChild(avisoEl);

    let restante = 3;
    const intervalo = setInterval(() => {
      restante--;
      const el = document.getElementById('inatividade-contador');
      if (el) el.textContent = restante;
      if (restante <= 0) clearInterval(intervalo);
    }, 1000);
    avisoEl._intervalo = intervalo;
  }

  function removerAviso() {
    if (avisoEl) {
      clearInterval(avisoEl._intervalo);
      avisoEl.remove();
      avisoEl = null;
    }
  }

  function iniciarTimers() {
    clearTimeout(timerLogout);
    clearTimeout(timerAviso);

    timerAviso = setTimeout(() => {
      criarAviso();
    }, TIMEOUT_MS - AVISO_MS);

    timerLogout = setTimeout(() => {
      window.location.href = '/logout?inatividade=1';
    }, TIMEOUT_MS);
  }

  window.resetInatividade = function () {
    removerAviso();
    iniciarTimers();
  };

  ['keydown', 'click', 'touchstart'].forEach(ev => {
    document.addEventListener(ev, () => {
      removerAviso();
      iniciarTimers();
    }, { passive: true });
  });

  iniciarTimers();
})();
