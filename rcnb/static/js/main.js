document.addEventListener('DOMContentLoaded', function() {
    // --- Mobile Navigation Active State ---
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.mobile-nav-item');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        // Simple check: if the current path starts with the link's path, it's active.
        // This handles cases like /profile/ and /profile/edit/ both highlighting the profile icon.
        if (currentPath.startsWith(linkPath)) {
            // Remove active from all others first to be safe
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });

    // A more specific check for the home page to avoid it always being active
    const homeLink = document.querySelector('.mobile-nav-item[href="/"]');
    if (currentPath === '/') {
        navLinks.forEach(l => l.classList.remove('active'));
        if(homeLink) homeLink.classList.add('active');
    }


    // --- Circle Toggle for old mobile menu (if it exists) ---
    const circleToggle = document.getElementById('circleToggle');
    const mobileNavMenu = document.querySelector('.mobile-nav'); // Assuming this is the old drawer

    if (circleToggle && mobileNavMenu) {
        circleToggle.addEventListener('click', () => {
            mobileNavMenu.classList.toggle('open');
            document.body.classList.toggle('menu-open');
        });
    }

    // --- Existing AJAX for Favorites & Cart ---
    function getCookie(name) {
        const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return match ? match.pop() : '';
    }

    // You might need to adjust selectors if your card structure changed
    document.querySelectorAll('.prod-btn.like, .icon-btn.like').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const favUrl = btn.dataset.favUrl;
            if (!favUrl) return;

            try {
                const res = await fetch(favUrl, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (res.status === 401) {
                    // Redirect or show login modal
                    window.location.href = '/users/login/';
                    return;
                }

                if (!res.ok) throw new Error(`Favorite toggle failed: ${res.status}`);

                const data = await res.json();
                btn.classList.toggle('active', data.is_favorited);
                // Simple visual feedback
                btn.style.transform = 'scale(1.2)';
                setTimeout(() => btn.style.transform = 'scale(1)', 150);
                 // Reload to see the change, simple but effective
                location.reload();

            } catch (err) {
                console.warn('Favorite toggle fetch failed', err);
            }
        });
    });

    document.querySelectorAll('.prod-btn.cart, .icon-btn.cart').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const url = btn.href;
            if (!url) return;
             try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: {
                      'X-CSRFToken': getCookie('csrftoken'),
                      'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                 if (res.status === 401) {
                    window.location.href = '/users/login/';
                    return;
                }
                // Visual feedback
                btn.style.transform = 'scale(1.2)';
                setTimeout(() => btn.style.transform = 'scale(1)', 150);

             } catch(err) {
                console.error("Error adding item to cart", err)
             }
        });
    });

});

document.addEventListener('DOMContentLoaded', function() {
    // --- Mobile Navigation Active State ---
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.mobile-nav-item');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        // More specific check to avoid multiple active states
        if (linkPath === currentPath) {
             link.classList.add('active');
        }
    });
    
    // --- Profile Edit Toggle ---
    const editProfileBtn = document.getElementById('edit-profile-btn');
    const profileForm = document.getElementById('profile-details-form');
    
    if (editProfileBtn && profileForm) {
        const viewElements = profileForm.querySelectorAll('[data-view]');
        const editElements = profileForm.querySelectorAll('[data-edit]');

        editProfileBtn.addEventListener('click', () => {
            viewElements.forEach(el => el.style.display = 'none');
            editElements.forEach(el => el.style.display = 'block');
        });
    }


    // --- Existing AJAX for Favorites & Cart ---
    function getCookie(name) {
        const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return match ? match.pop() : '';
    }

    document.querySelectorAll('.icon-btn.like').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const favUrl = btn.dataset.favUrl;
            if (!favUrl) return;

            try {
                const res = await fetch(favUrl, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (res.status === 401) {
                    window.location.href = '/users/login/';
                    return;
                }

                if (!res.ok) throw new Error(`Favorite toggle failed: ${res.status}`);

                const data = await res.json();
                btn.classList.toggle('active', data.is_favorited);
                
                // Optional: Reload to see change reflected in favorites list immediately
                if(window.location.pathname.includes('/favorites/')) {
                    location.reload();
                }

            } catch (err) {
                console.warn('Favorite toggle fetch failed', err);
            }
        });
    });

    document.querySelectorAll('.icon-btn.cart').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const url = btn.href;
            if (!url) return;
             try {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: {
                      'X-CSRFToken': getCookie('csrftoken'),
                      'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                 if (res.status === 401) {
                    window.location.href = '/users/login/';
                    return;
                }
                
                // Simple visual feedback
                btn.style.transform = 'scale(1.2)';
                setTimeout(() => btn.style.transform = 'scale(1)', 150);
                
                // You could update a cart count here if you have one
                
             } catch(err) {
                console.error("Error adding item to cart", err)
             }
        });
    });

});
