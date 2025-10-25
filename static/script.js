(function () {
  const menuBtn = document.getElementById('menuBtn');
  const sidebar = document.getElementById('sidebar');
  if (!menuBtn || !sidebar) return;

  function toggle() {
    const open = sidebar.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
  }

  menuBtn.addEventListener('click', toggle);

  // Close sidebar on outside click for small screens
  document.addEventListener('click', (e) => {
    const within = sidebar.contains(e.target) || menuBtn.contains(e.target);
    if (!within && sidebar.classList.contains('open')) sidebar.classList.remove('open');
  });
})();