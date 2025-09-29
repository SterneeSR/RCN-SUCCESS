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

document.addEventListener('DOMContentLoaded', () => {
    // --- Element Selections ---
    const header = document.getElementById('main-header');
    const circleToggle = document.getElementById('circleToggle');
    const desktopNav = document.querySelector('nav.navbar');
    
    // --- State ---
    let mobileNav = null;
    const scrollThreshold = 50;
    const circleActiveColors = ['#F97316', '#FBBF24', '#22C55E', '#F43F5E']; // Orange, Yellow, Green, Rose

    // --- Functions ---
    const handleScroll = () => {
        if (window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    const createMobileNav = () => {
        if (!mobileNav && desktopNav) {
            // Clone desktop nav to create the mobile nav dynamically
            mobileNav = desktopNav.cloneNode(true);
            mobileNav.classList.remove('navbar');
            mobileNav.classList.add('mobile-nav');
            mobileNav.id = 'mobileNav';
            document.body.appendChild(mobileNav);
        }
    };

    const toggleMobileMenu = () => {
        createMobileNav();
        
        const isOpen = mobileNav.classList.toggle('open');
        document.body.classList.toggle('menu-open', isOpen);
        circleToggle.setAttribute('aria-expanded', isOpen);

        const circles = document.querySelectorAll('.circle-toggle .circle');
        
        // Trigger pulse animation
        circles.forEach(circle => {
            circle.classList.add('animate-pulse');
            setTimeout(() => circle.classList.remove('animate-pulse'), 400);
        });

        // Toggle circle colors
        circles.forEach((circle, idx) => {
            if (isOpen) {
                circle.style.backgroundColor = circleActiveColors[idx];
                circle.style.borderColor = circleActiveColors[idx];
            } else {
                circle.style.backgroundColor = 'transparent';
                circle.style.borderColor = '#fff';
            }
        });
    };

    const closeMobileMenu = () => {
        if (mobileNav && mobileNav.classList.contains('open')) {
            toggleMobileMenu();
        }
    };

    // --- Event Listeners ---
    if (header) { // Only add scroll listener if header exists on the page
        window.addEventListener('scroll', handleScroll);
        handleScroll(); // Check scroll on page load
    }
    if (circleToggle) {
        circleToggle.addEventListener('click', toggleMobileMenu);
    }

    // Close menu when clicking outside or on a link
    document.addEventListener('click', (e) => {
        if (!mobileNav || !mobileNav.classList.contains('open')) return;
        const isLinkClick = e.target.closest('.mobile-nav .nav-menu a');
        const isOutsideClick = !e.target.closest('.mobile-nav') && !e.target.closest('.circle-toggle');
        if (isLinkClick || isOutsideClick) {
            closeMobileMenu();
        }
    });

    // --- Auto-hide Django Messages ---
    const messagesContainer = document.querySelector('.messages-container');
    if (messagesContainer) {
        setTimeout(() => {
            messagesContainer.style.transition = 'opacity 0.5s';
            messagesContainer.style.opacity = '0';
            setTimeout(() => messagesContainer.remove(), 500);
        }, 4000);
    }

    // --- Initializations ---
    lucide.createIcons(); // Render all Lucide icons
});

/* ================ MEMBERSHIP PAGE ================ */

// Membership page specific JavaScript functionality

class MembershipPage {
    constructor() {
        this.hoveredIcon = null;
        this.currentIconText = "Choose a membership type to see details";
        this.iconData = [
            {
                description: "Different membership tiers available for students, professionals, and institutions",
                colorStart: "#8b5cf6",
                colorEnd: "#7c3aed"
            },
            {
                description: "Annual membership with renewable benefits and continuous access to resources",
                colorStart: "#f59e0b",
                colorEnd: "#d97706"
            },
            {
                description: "Grace period for renewal ensures uninterrupted access to all member benefits",
                colorStart: "#10b981",
                colorEnd: "#059669"
            }
        ];
        this.init();
    }

    init() {
        this.setupInteractiveIcons();
        this.setupNetworkingCards();
        this.setupAnimations();
        this.setupResponsiveTable();
    }

    setupInteractiveIcons() {
        const iconItems = document.querySelectorAll('.icon-item');
        const descriptionElement = document.getElementById('icon-description');

        iconItems.forEach((item, index) => {
            const iconElement = item.querySelector('.interactive-icon');
            
            // Desktop events
            item.addEventListener('mouseenter', () => {
                this.handleIconHover(index, iconElement, descriptionElement);
            });

            item.addEventListener('mouseleave', () => {
                this.handleIconLeave(iconElement, descriptionElement);
            });

            // Mobile events
            item.addEventListener('touchstart', (e) => {
                e.preventDefault();
                if (this.hoveredIcon === index) {
                    this.handleIconLeave(iconElement, descriptionElement);
                } else {
                    this.handleIconHover(index, iconElement, descriptionElement);
                }
            });

            item.addEventListener('click', (e) => {
                e.preventDefault();
                if (this.hoveredIcon === index) {
                    this.handleIconLeave(iconElement, descriptionElement);
                } else {
                    this.handleIconHover(index, iconElement, descriptionElement);
                }
            });
        });
    }

    handleIconHover(index, iconElement, descriptionElement) {
        this.hoveredIcon = index;
        const data = this.iconData[index];
        
        // Update icon styling
        iconElement.style.background = `linear-gradient(135deg, ${data.colorStart}, ${data.colorEnd})`;
        iconElement.style.color = 'white';
        iconElement.style.boxShadow = '0 15px 35px rgba(139, 92, 246, 0.3), 0 5px 15px rgba(0, 0, 0, 0.2)';
        
        // Update description text
        if (descriptionElement) {
            descriptionElement.textContent = data.description;
        }

        // Add orbit animation
        const orbit = iconElement.querySelector('.icon-orbit');
        if (orbit) {
            orbit.style.opacity = '0.5';
            orbit.style.borderColor = 'rgba(255, 255, 255, 0.3)';
        }
    }

    handleIconLeave(iconElement, descriptionElement) {
        this.hoveredIcon = null;
        
        // Reset icon styling
        const isDark = document.body.classList.contains('dark');
        iconElement.style.background = isDark 
            ? 'linear-gradient(135deg, #374151, #1f2937)'
            : 'linear-gradient(135deg, #e5e7eb, #d1d5db)';
        iconElement.style.color = '#6b7280';
        iconElement.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
        
        // Reset description text
        if (descriptionElement) {
            descriptionElement.textContent = this.currentIconText;
        }

        // Remove orbit animation
        const orbit = iconElement.querySelector('.icon-orbit');
        if (orbit) {
            orbit.style.opacity = '0';
            orbit.style.borderColor = 'transparent';
        }
    }

    setupNetworkingCards() {
        const networkingCards = document.querySelectorAll('.networking-card');
        
        networkingCards.forEach((card, index) => {
            // Add staggered animation delay
            card.style.animationDelay = `${index * 0.1}s`;
            
            // Enhanced hover effects
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'scale(1.05) translateY(-0.5rem) rotate(1deg)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'scale(1) translateY(0) rotate(0deg)';
            });
        });

        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.2,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.animation = 'slideInFromBottom 0.6s ease-out forwards';
                        entry.target.style.opacity = '1';
                    }, index * 100);
                }
            });
        }, observerOptions);

        networkingCards.forEach(card => {
            card.style.opacity = '0';
            observer.observe(card);
        });
    }

    setupAnimations() {
        // Setup nano decorations with random animations
        const nanoDecorations = document.querySelectorAll('.nano-decoration .nano-dot');
        
        nanoDecorations.forEach((dot, index) => {
            const delay = Math.random() * 2;
            dot.style.animationDelay = `${delay}s`;
        });

        // Setup milestone card animations with staggered delays
        const milestoneCards = document.querySelectorAll('.fee-card, .fee-table tbody tr');
        
        milestoneCards.forEach((card, index) => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'scale(1.02)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'scale(1)';
            });
        });

        // Add entrance animations for sections
        this.setupSectionAnimations();
    }

    setupSectionAnimations() {
        const sections = document.querySelectorAll('section');
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
                }
            });
        }, observerOptions);

        sections.forEach(section => {
            observer.observe(section);
        });
    }

    setupResponsiveTable() {
        // Handle responsive table switching
        const handleResize = () => {
            const desktopTable = document.querySelector('.desktop-table');
            const mobileCards = document.querySelector('.mobile-cards');
            
            if (window.innerWidth >= 768) {
                if (desktopTable) {
                    desktopTable.style.display = 'block';
                    desktopTable.style.visibility = 'visible';
                }
                if (mobileCards) {
                    mobileCards.style.display = 'none';
                    mobileCards.style.visibility = 'hidden';
                }
            } else {
                if (desktopTable) {
                    desktopTable.style.display = 'none';
                    desktopTable.style.visibility = 'hidden';
                }
                if (mobileCards) {
                    mobileCards.style.display = 'block';
                    mobileCards.style.visibility = 'visible';
                }
            }
        };

        // Initial setup with delay to ensure DOM is ready
        setTimeout(handleResize, 100);
        
        // Handle resize events
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(handleResize, 250);
        });

        // Force initial state on load
        window.addEventListener('load', handleResize);
    }

    // Method to handle dark mode changes
    updateTheme() {
        // Re-setup icon styling for theme change
        if (this.hoveredIcon === null) {
            const iconElements = document.querySelectorAll('.interactive-icon');
            iconElements.forEach(iconElement => {
                const isDark = document.body.classList.contains('dark');
                iconElement.style.background = isDark 
                    ? 'linear-gradient(135deg, #374151, #1f2937)'
                    : 'linear-gradient(135deg, #e5e7eb, #d1d5db)';
            });
        }
    }

    // Method to handle responsive adjustments
    handleResize() {
        this.setupResponsiveTable();
    }
}

// Initialize membership page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
   if (document.body.classList.contains('membership-page')) {
        const membershipPage = new MembershipPage();
        
        // Handle resize events
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                membershipPage.handleResize();
            }, 250);
        });

        // Handle theme changes
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    membershipPage.updateTheme();
                }
            });
        });

        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['class']
        });
    }
});

// CSS Animation additions
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInFromBottom {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .networking-card {
        animation: slideInFromBottom 0.6s ease-out forwards;
    }
    
    .development-item {
        transition: all 0.3s ease;
    }
    
    .development-item:hover {
        transform: translateX(10px);
    }
    
    .interactive-icon {
        will-change: transform, background, box-shadow;
    }
    
    .fee-card,
    .fee-table tbody tr {
        will-change: transform;
    }
`;
document.head.appendChild(style);

document.head.appendChild(style);

/* ================ Carousel ================ */

/* ================ Generic Carousel Initializer ================ */

function initializeCarousel(carouselElement, arrowButtons) {
    // Return early if the carousel or its cards are not found
    if (!carouselElement || !carouselElement.querySelector(".card, .image-card")) {
        console.error("Carousel element or its cards not found.", carouselElement);
        return;
    }

    const firstCard = carouselElement.querySelector(".card, .image-card");
    // Add a fallback in case offsetWidth is 0 for some reason
    const firstCardWidth = firstCard.offsetWidth > 0 ? firstCard.offsetWidth : 250; 
    const carouselChildrens = [...carouselElement.children];

    let isDragging = false, isAutoPlay = true, startX, startScrollLeft, timeoutId;

    // Get the number of cards to clone for a seamless loop effect
    const cardsToClone = Math.round(carouselElement.offsetWidth / firstCardWidth);

    // Clone first few cards and add to the end
    if (carouselChildrens.length > cardsToClone) {
        carouselChildrens.slice(0, cardsToClone).forEach(card => {
            carouselElement.insertAdjacentHTML("beforeend", card.outerHTML);
        });

        // Clone last few cards and add to the beginning
        carouselChildrens.slice(-cardsToClone).forEach(card => {
            carouselElement.insertAdjacentHTML("afterbegin", card.outerHTML);
        });
    }


    // Add event listeners for the arrow buttons
    arrowButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // *** FIX: Check for class instead of ID for more robust arrow logic ***
            // This works even if IDs are duplicated across carousels.
            if (btn.classList.contains("fa-angle-left")) {
                carouselElement.scrollLeft -= firstCardWidth;
            } else {
                carouselElement.scrollLeft += firstCardWidth;
            }
        });
    });

    const dragStart = (e) => {
        isDragging = true;
        carouselElement.classList.add("dragging");
        startX = e.pageX;
        startScrollLeft = carouselElement.scrollLeft;
    }

    const dragging = (e) => {
        if (!isDragging) return;
        carouselElement.scrollLeft = startScrollLeft - (e.pageX - startX);
    }

    const dragStop = () => {
        isDragging = false;
        carouselElement.classList.remove("dragging");
    }

    const infiniteScroll = () => {
        if (carouselElement.scrollLeft === 0) {
            carouselElement.classList.add("no-transition");
            carouselElement.scrollLeft = carouselElement.scrollWidth - (2 * carouselElement.offsetWidth);
            carouselElement.classList.remove("no-transition");
        }
        else if (Math.ceil(carouselElement.scrollLeft) >= carouselElement.scrollWidth - carouselElement.offsetWidth) {
            carouselElement.classList.add("no-transition");
            carouselElement.scrollLeft = carouselElement.offsetWidth;
            carouselElement.classList.remove("no-transition");
        }

        clearTimeout(timeoutId);
        if (!carouselElement.matches(":hover")) autoPlay();
    }

    const autoPlay = () => {
        // Autoplay is disabled on screens smaller than 800px or when user is hovering
        if (window.innerWidth < 800) return;
        
        // *** CHANGE: Reduced timeout from 2500ms to 2000ms for faster autoplay ***
        timeoutId = setTimeout(() => carouselElement.scrollLeft += firstCardWidth, 2000);
    }
    
    autoPlay(); // Start the autoplay

    carouselElement.addEventListener("mousedown", dragStart);
    carouselElement.addEventListener("mousemove", dragging);
    document.addEventListener("mouseup", dragStop);
    carouselElement.addEventListener("scroll", infiniteScroll);
    carouselElement.addEventListener("mouseenter", () => clearTimeout(timeoutId));
    carouselElement.addEventListener("mouseleave", autoPlay);
}

// ==================================================================================
//  Initialize ALL carousels on the site when the page loads
// ==================================================================================
document.addEventListener("DOMContentLoaded", () => {
    const carouselContainers = document.querySelectorAll(".wrapper, .image-carousel-wrapper");

    carouselContainers.forEach(container => {
        const carousel = container.querySelector(".tcarousel-1, .image-carousel");
        // This selector correctly finds the Font Awesome icons used as buttons
        const arrowBtns = container.querySelectorAll(".fa-solid.fa-angle-left, .fa-solid.fa-angle-right");

        if (carousel && arrowBtns.length > 0) {
            initializeCarousel(carousel, arrowBtns);
        } else {
            console.warn("A carousel container was found, but it is missing the carousel list or arrow buttons.", container);
        }
    });
});

/* ================ Events JS ================ */

document.addEventListener('DOMContentLoaded', function () {
    // Logic for "Read More" links
    document.querySelectorAll('.read-more-trigger').forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const container = this.closest('.card-description-container');
            if (container) {
                const shortDescription = container.querySelector('.description-short');
                const fullDescription = container.querySelector('.description-full');
                if (shortDescription && fullDescription) {
                    shortDescription.style.display = 'none';
                    fullDescription.style.maxHeight = fullDescription.scrollHeight + 'px';
                }
            }
        });
    });

    // Logic for "View All" buttons
    document.querySelectorAll('.view-all-btn').forEach(button => {
        button.addEventListener('click', function() {
            const sectionId = this.dataset.section;
            const section = document.getElementById(sectionId);
            if (section) {
                section.querySelectorAll('.hidden-card').forEach(card => {
                    card.style.display = 'flex'; // Use flex as the card is a flex container
                    card.classList.remove('hidden-card');
                });
                this.style.display = 'none'; // Hide the button after clicking
            }
        });
    });
});