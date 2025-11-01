    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');
    const userProfile = document.getElementById('userProfile');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const mainContent = document.getElementById('mainContent');

    // ✅ Par défaut, la sidebar reste affichée (pas de flash)
    let sidebarVisible = true;

//    menuToggle.addEventListener('click', () => {
  //    if (window.innerWidth <= 768) {
    //    sidebarVisible = !sidebarVisible;
      //  sidebar.classList.toggle('hidden', !sidebarVisible);
//      } else {
  //      sidebar.classList.toggle('collapsed');
    //  }
    //});

    // Toggle user dropdown
    userProfile.addEventListener('click', () => {
      dropdownMenu.classList.toggle('active');
    });

    // // Simulated navigation
    // document.querySelectorAll('.sidebar ul li').forEach(item => {
    //   item.addEventListener('click', () => {
    //     const page = item.getAttribute('data-page');
    //     mainContent.innerHTML = `
    //       <h2>${page.charAt(0).toUpperCase() + page.slice(1)}</h2>
    //       <p>Contenu dynamique pour la section <b>${page}</b>.</p>
    //     `;
    //   });
    // });

    // Fermer dropdown si clic en dehors
    window.addEventListener('click', (e) => {
      if (!userProfile.contains(e.target)) {
        dropdownMenu.classList.remove('active');
      }
    });