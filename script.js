// Proteção visual de demonstração: exige que o login desta sessão tenha sido feito.
if (sessionStorage.getItem("estoquepro_logged_in") !== "true") {
  window.location.replace("index.html");
}

const logoutButton = document.getElementById("logoutButton");
if (logoutButton) {
  logoutButton.addEventListener("click", () => {
    sessionStorage.removeItem("estoquepro_logged_in");
    sessionStorage.removeItem("estoquepro_user");
    window.location.replace("index.html");
  });
}

const navItems = document.querySelectorAll(".nav-item");
const pageTitle = document.getElementById("pageTitle");
const headingTitle = document.getElementById("headingTitle");
const toast = document.getElementById("toast");
const sidebar = document.getElementById("sidebar");
const menuToggle = document.getElementById("menuToggle");

const now = new Date();
document.getElementById("today").textContent = now.toLocaleDateString("pt-BR", {
  day: "2-digit", month: "long", year: "numeric"
});

let toastTimer;
function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2600);
}

navItems.forEach((item) => {
  item.addEventListener("click", () => {
    navItems.forEach((nav) => nav.classList.remove("active"));
    item.classList.add("active");

    const page = item.dataset.page;
    pageTitle.textContent = page;
    headingTitle.textContent = page;

    if (page !== "Dashboard") {
      showToast(`A tela "${page}" será desenvolvida em uma próxima etapa.`);
    }
    sidebar.classList.remove("open");
  });
});

menuToggle.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

document.addEventListener("click", (event) => {
  if (window.innerWidth <= 760 &&
      sidebar.classList.contains("open") &&
      !sidebar.contains(event.target) &&
      !menuToggle.contains(event.target)) {
    sidebar.classList.remove("open");
  }
});

document.querySelectorAll(".text-link").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    showToast("Essa funcionalidade será implementada na próxima etapa.");
  });
});
