// Main JavaScript - Shared functionality across all pages

// ============================================
// THEME MANAGEMENT
// ============================================
class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'light';
    this.init();
  }

  init() {
    this.applyTheme();
    this.setupToggle();
  }

  applyTheme() {
    document.documentElement.setAttribute('data-theme', this.theme);
    this.updateToggleIcon();
  }

  toggle() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.theme);
    this.applyTheme();
  }

  updateToggleIcon() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.textContent = this.theme === 'light' ? '🌙' : '☀️';
    }
  }

  setupToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => this.toggle());
    }
  }
}

// ============================================
// MOBILE MENU
// ============================================
class MobileMenu {
  constructor() {
    this.init();
  }

  init() {
    const toggle = document.getElementById('mobile-menu-toggle');
    const menu = document.getElementById('navbar-nav');

    if (toggle && menu) {
      toggle.addEventListener('click', () => {
        menu.classList.toggle('show');
        const isOpen = menu.classList.contains('show');
        toggle.textContent = isOpen ? '✕' : '☰';
      });

      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !menu.contains(e.target)) {
          menu.classList.remove('show');
          toggle.textContent = '☰';
        }
      });

      // Close menu when clicking a link
      menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          menu.classList.remove('show');
          toggle.textContent = '☰';
        });
      });
    }
  }
}

// ============================================
// NAVIGATION ACTIVE STATE
// ============================================
class NavigationManager {
  constructor() {
    this.init();
  }

  init() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.navbar-link');

    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentPage) {
        link.classList.add('active');
      }
    });
  }
}

// ============================================
// SMOOTH SCROLL
// ============================================
class SmoothScroll {
  constructor() {
    this.init();
  }

  init() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (href === '#') return;

        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }
}

// ============================================
// ANIMATIONS ON SCROLL
// ============================================
class ScrollAnimations {
  constructor() {
    this.init();
  }

  init() {
    const options = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in');
          observer.unobserve(entry.target);
        }
      });
    }, options);

    document.querySelectorAll('.card, .stat, .grid > *').forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  }
}

// ============================================
// PROGRESS BAR ANIMATIONS
// ============================================
class ProgressAnimator {
  static animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const bar = entry.target;
          const targetWidth = bar.getAttribute('data-width') || '0%';

          // Animate from 0 to target width
          setTimeout(() => {
            bar.style.width = targetWidth;
          }, 100);

          observer.unobserve(bar);
        }
      });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => {
      const width = bar.style.width;
      bar.setAttribute('data-width', width);
      bar.style.width = '0%';
      observer.observe(bar);
    });
  }
}

// ============================================
// NUMBER COUNTER ANIMATION
// ============================================
class NumberCounter {
  static animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16); // 60fps
    let current = start;

    const timer = setInterval(() => {
      current += increment;
      if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
        current = end;
        clearInterval(timer);
      }
      element.textContent = Math.round(current);
    }, 16);
  }

  static init() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          const endValue = parseInt(element.getAttribute('data-value'));
          this.animateValue(element, 0, endValue, 2000);
          observer.unobserve(element);
        }
      });
    }, { threshold: 0.5 });

    document.querySelectorAll('[data-animate-number]').forEach(el => {
      observer.observe(el);
    });
  }
}

// ============================================
// TOOLTIP
// ============================================
class Tooltip {
  static init() {
    document.querySelectorAll('[data-tooltip]').forEach(element => {
      element.addEventListener('mouseenter', (e) => {
        const text = element.getAttribute('data-tooltip');
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
          position: absolute;
          background: var(--color-text-primary);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 0.375rem;
          font-size: 0.875rem;
          white-space: nowrap;
          pointer-events: none;
          z-index: var(--z-tooltip);
          box-shadow: var(--shadow-lg);
        `;
        document.body.appendChild(tooltip);

        const updatePosition = (e) => {
          tooltip.style.left = e.pageX + 10 + 'px';
          tooltip.style.top = e.pageY + 10 + 'px';
        };

        updatePosition(e);
        element.addEventListener('mousemove', updatePosition);

        element.addEventListener('mouseleave', () => {
          tooltip.remove();
        }, { once: true });
      });
    });
  }
}

// ============================================
// PRINT FUNCTIONALITY
// ============================================
class PrintManager {
  static setupPrintButtons() {
    document.querySelectorAll('[data-print]').forEach(btn => {
      btn.addEventListener('click', () => window.print());
    });
  }
}

// ============================================
// SHARE FUNCTIONALITY
// ============================================
class ShareManager {
  static async share(title, text, url) {
    if (navigator.share) {
      try {
        await navigator.share({ title, text, url });
      } catch (err) {
        console.log('Share cancelled or failed:', err);
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(url);
      alert('Link copied to clipboard!');
    }
  }

  static setupShareButtons() {
    document.querySelectorAll('[data-share]').forEach(btn => {
      btn.addEventListener('click', () => {
        this.share(
          'Health Optimization Dashboard',
          'Check out my health optimization progress!',
          window.location.href
        );
      });
    });
  }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================
const utils = {
  // Format numbers with commas
  formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  },

  // Calculate percentage
  calculatePercentage(value, max) {
    return Math.round((value / max) * 100);
  },

  // Get status color based on value and thresholds
  getStatusColor(value, optimal, reference) {
    if (value >= optimal.min && value <= optimal.max) return 'var(--color-success)';
    if (value >= reference.min && value <= reference.max) return 'var(--color-warning)';
    return 'var(--color-danger)';
  },

  // Debounce function
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  // Local storage helpers
  storage: {
    set(key, value) {
      localStorage.setItem(key, JSON.stringify(value));
    },
    get(key) {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    },
    remove(key) {
      localStorage.removeItem(key);
    }
  }
};

// ============================================
// ACCESSIBILITY ENHANCEMENTS
// ============================================
class AccessibilityManager {
  static init() {
    // Skip to main content
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'sr-only';
    skipLink.textContent = 'Skip to main content';
    skipLink.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      padding: 1rem;
      background: var(--color-primary);
      color: white;
      z-index: 9999;
    `;
    skipLink.addEventListener('focus', () => {
      skipLink.classList.remove('sr-only');
    });
    skipLink.addEventListener('blur', () => {
      skipLink.classList.add('sr-only');
    });
    document.body.insertBefore(skipLink, document.body.firstChild);

    // Keyboard navigation for cards
    document.querySelectorAll('.card').forEach(card => {
      if (!card.hasAttribute('tabindex')) {
        card.setAttribute('tabindex', '0');
      }
    });
  }

  // Announce to screen readers
  static announce(message, priority = 'polite') {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', priority);
    announcement.className = 'sr-only';
    announcement.textContent = message;
    document.body.appendChild(announcement);
    setTimeout(() => announcement.remove(), 1000);
  }
}

// ============================================
// INITIALIZE ALL COMPONENTS
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  // Core functionality
  new ThemeManager();
  new MobileMenu();
  new NavigationManager();
  new SmoothScroll();

  // Animations
  new ScrollAnimations();
  ProgressAnimator.animateProgressBars();
  NumberCounter.init();

  // Interactive elements
  Tooltip.init();
  PrintManager.setupPrintButtons();
  ShareManager.setupShareButtons();

  // Accessibility
  AccessibilityManager.init();

  // Reduce motion for accessibility
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    document.documentElement.style.setProperty('--transition-fast', '0.01ms');
    document.documentElement.style.setProperty('--transition-base', '0.01ms');
    document.documentElement.style.setProperty('--transition-slow', '0.01ms');
  }
});

// Export utilities for use in other scripts
window.utils = utils;
window.AccessibilityManager = AccessibilityManager;
