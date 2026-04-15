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

  function validarEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  window.showTab = showTab;

  window.fazerLogin = () => {
    const email = document.getElementById("login-email").value.trim();
    const senha = document.getElementById("login-senha").value;
    if (!email || !senha) {
      mostrarMsg(loginMsg, "Preencha todos os campos.", "erro");
      return;
    }
    if (!validarEmail(email)) {
      mostrarMsg(loginMsg, "E-mail inválido.", "erro");
      return;
    }
    mostrarMsg(loginMsg, "Login realizado com sucesso! Redirecionando...", "sucesso");
    setTimeout(() => {
      window.location.href = "the-keep-profile.html";
    }, 1200);
  };

  window.fazerCadastro = () => {
    const nome = document.getElementById("cad-nome").value.trim();
    const email = document.getElementById("cad-email").value.trim();
    const senha = document.getElementById("cad-senha").value;
    const confirmar = document.getElementById("cad-confirmar").value;
    if (!nome || !email || !senha || !confirmar) {
      mostrarMsg(signupMsg, "Preencha todos os campos.", "erro");
      return;
    }
    if (!validarEmail(email)) {
      mostrarMsg(signupMsg, "E-mail inválido.", "erro");
      return;
    }
    if (senha.length < 6) {
      mostrarMsg(signupMsg, "A senha precisa ter pelo menos 6 caracteres.", "erro");
      return;
    }
    if (senha !== confirmar) {
      mostrarMsg(signupMsg, "As senhas não coincidem.", "erro");
      return;
    }
    mostrarMsg(signupMsg, "Conta criada com sucesso! Redirecionando...", "sucesso");
    setTimeout(() => {
      window.location.href = "the-keep-profile.html";
    }, 1200);
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
