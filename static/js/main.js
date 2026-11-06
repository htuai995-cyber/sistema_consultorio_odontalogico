/* Sonrisa Perfecta - JavaScript principal */

// Auto-dismiss alerts after 5s
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });

  // Alert close buttons
  document.querySelectorAll('.alert-close').forEach(btn => {
    btn.addEventListener('click', function () {
      const alert = this.closest('.alert');
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    });
  });

  // Sidebar toggle for mobile
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  // Active nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath ||
        (currentPath !== '/' && link.getAttribute('href') !== '/' && currentPath.startsWith(link.getAttribute('href')))) {
      link.classList.add('active');
    }
  });

  // Remember me (mantener cuenta abierta)
  const rememberMe = document.getElementById('id_remember_me');
  if (rememberMe) {
    const saved = localStorage.getItem('rememberMe');
    if (saved === 'true') rememberMe.checked = true;
    rememberMe.addEventListener('change', function () {
      localStorage.setItem('rememberMe', this.checked);
    });
  }

  // Confirm delete modals
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) e.preventDefault();
    });
  });
});

// PDF download with filter params
function descargarPDF(baseUrl) {
  const params = new URLSearchParams(window.location.search);
  window.open(baseUrl + '?' + params.toString(), '_blank');
}

// Print page
function imprimirPagina() {
  window.print();
}

