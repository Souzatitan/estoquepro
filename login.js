const form = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const errorMessage = document.getElementById("errorMessage");
const togglePassword = document.getElementById("togglePassword");

const DEMO_EMAIL = "admin@estoquepro.com";
const DEMO_PASSWORD = "admin123";

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const email = emailInput.value.trim().toLowerCase();
  const password = passwordInput.value;

  if (email === DEMO_EMAIL && password === DEMO_PASSWORD) {
    // Apenas demonstração de navegação. Não é autenticação segura.
    sessionStorage.setItem("estoquepro_logged_in", "true");
    sessionStorage.setItem("estoquepro_user", "Anderson Souza");
    window.location.href = "dashboard.html";
    return;
  }

  errorMessage.textContent = "Usuário ou senha incorretos. Confira os dados demonstrativos.";
});

togglePassword.addEventListener("click", () => {
  const showing = passwordInput.type === "text";
  passwordInput.type = showing ? "password" : "text";
  togglePassword.setAttribute("aria-label", showing ? "Mostrar senha" : "Ocultar senha");
});

document.getElementById("forgotLink").addEventListener("click", (event) => {
  event.preventDefault();
  errorMessage.textContent = "Recuperação de senha será conectada ao sistema posteriormente.";
});
