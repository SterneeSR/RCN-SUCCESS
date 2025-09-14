(function () {
  'use strict';

  // --- UTILS ---
  function getCookie(name) {
    const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return match ? match.pop() : '';
  }

// animation for like/cart button clicks //

  function makeRadialOverlay(card, x, y, type) {
    if (!card) return;
    card.querySelectorAll('.swipe-overlay').forEach(el => el.remove());

    const overlay = document.createElement('div');
    overlay.className = `swipe-overlay radial swipe-${type}`;
    overlay.style.left = `${x}px`;
    overlay.style.top = `${y}px`;
    card.appendChild(overlay);

    overlay.addEventListener('animationend', () => overlay.remove(), { once: true });
  }

  function getCoords(btn) {
    const card = btn.closest('.product-card');
    if (!card) return { x: 20, y: 20, card: null };

    const rect = card.getBoundingClientRect();
    const brect = btn.getBoundingClientRect();
    return {
      x: brect.left - rect.left + brect.width / 2,
      y: brect.top - rect.top + brect.height / 2,
      card
    };
  }

  // --- LOGIN MODAL HANDLERS ---
  const loginModal = document.getElementById('login-prompt-modal');
  const closeModalBtn = document.getElementById('close-modal-btn');

  function showLoginModal() {
    if (loginModal) loginModal.style.display = 'flex';
  }

  function hideLoginModal() {
    if (loginModal) loginModal.style.display = 'none';
  }

  if (closeModalBtn) closeModalBtn.addEventListener('click', hideLoginModal);
  if (loginModal) {
    loginModal.addEventListener('click', function (event) {
      if (event.target === loginModal) hideLoginModal();
    });
  }

  // --- FAVORITE BUTTON HANDLER ---
  async function handleFavoriteClick(btn) {
    const favUrl = btn.dataset.favUrl;
    if (!favUrl) return;

    const { x, y, card } = getCoords(btn);
    makeRadialOverlay(card, x, y, 'like');

    try {
      const res = await fetch(favUrl, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      });

      if (res.status === 401) {
        showLoginModal();
        return;
      }

      if (!res.ok) return console.error(`Favorite toggle failed: ${res.status}`);

      const data = await res.json();
      const isFavorited = data.is_favorited;

      btn.classList.toggle('active', isFavorited);
      btn.setAttribute('aria-pressed', isFavorited);

      const icon = btn.querySelector('i.fa-heart');
      if (icon) icon.style.color = isFavorited ? 'red' : '';
    } catch (err) {
      console.warn('Favorite toggle fetch failed', err);
    }
  }

  // --- CART BUTTON HANDLER ---
  async function handleCartClick(btn) {
    const url = btn.href;
    if (!url) return;

    const { x, y, card } = getCoords(btn);
    makeRadialOverlay(card, x, y, 'cart');

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
      });

      if (res.status === 401) {
        showLoginModal();
        return;
      }

      const data = await res.json();
      if (data.success) {
        console.log(`"${data.message}"`);
      }
    } catch (err) {
      console.error('Error adding item to cart:', err);
    }
  }

  // --- INIT ---
  function init() {
    document.querySelectorAll('.prod-btn.like').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        handleFavoriteClick(btn);
      });
    });

    document.querySelectorAll('.prod-btn.cart').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        handleCartClick(btn);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();


/* --- HEADER BEHAVIOUR --- */

