document.addEventListener("DOMContentLoaded", () => {
  const loginTab = document.getElementById("tab-login");
  const signupTab = document.getElementById("tab-cadastro");
  const loginForm = document.getElementById("form-login");
  const signupForm = document.getElementById("form-cadastro");
  const loginMsg = document.getElementById("login-msg");
  const signupMsg = document.getElementById("cadastro-msg");

  function showTab(tab) {
    const isLogin = tab === "login";
    loginForm.style.display = isLogin ? "flex" : "none";
    signupForm.style.display = isLogin ? "none" : "flex";
    loginTab.classList.toggle("active", isLogin);
    signupTab.classList.toggle("active", !isLogin);
    limparMensagens();
  }

  function limparMensagens() {
    [loginMsg, signupMsg].forEach((el) => {
      el.style.display = "none";
      el.className = "msg";
      el.textContent = "";
    });
  }

  function mostrarMsg(el, texto, tipo) {
    el.textContent = texto;
    el.className = `msg ${tipo}`;
    el.style.display = "block";
  }

  function redirecionarPerfil(el, texto) {
    mostrarMsg(el, texto, "sucesso");
    setTimeout(() => {
      window.location.href = "the-keep-profile.html";
    }, 700);
  }

  window.showTab = showTab;

  window.fazerLogin = () => {
    const email = document.getElementById("login-email").value.trim();
    const senha = document.getElementById("login-senha").value.trim();

    if (!email || !senha) {
      mostrarMsg(loginMsg, "Preencha e-mail e senha para continuar.", "erro");
      return;
    }

    redirecionarPerfil(loginMsg, "Login de simulação realizado! Redirecionando...");
  };

  window.fazerCadastro = () => {
    const nome = document.getElementById("cad-nome").value.trim();
    const email = document.getElementById("cad-email").value.trim();
    const senha = document.getElementById("cad-senha").value.trim();
    const confirmar = document.getElementById("cad-confirmar").value.trim();

    if (!nome || !email || !senha || !confirmar) {
      mostrarMsg(signupMsg, "Preencha todos os campos para continuar.", "erro");
      return;
    }

    redirecionarPerfil(signupMsg, "Cadastro de simulação criado! Redirecionando...");
  };

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;
    const loginVisible = loginForm.style.display !== "none";
    if (loginVisible) {
      window.fazerLogin();
    } else {
      window.fazerCadastro();
    }
  });
});
