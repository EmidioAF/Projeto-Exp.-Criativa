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

// ---------- Logout automático por inatividade ----------
// TODO: Implementar via middleware no backend para maior segurança.
// Esta versão client-side redireciona após 30min de inatividade.
(function () {
  const TIMEOUT = 30 * 60 * 1000; // 30 minutos
  let timer;
  function reset() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (document.cookie.includes('session')) {
        window.location.href = '/logout?inatividade=1';
      }
    }, TIMEOUT);
  }
  ['mousemove', 'keydown', 'click', 'scroll', 'touchstart'].forEach(e => {
    document.addEventListener(e, reset, { passive: true });
  });
  reset();
})();
