/* ═══════════════════════════════════════════════════════════════
   MINI ZERODHA - MAIN JAVASCRIPT
   ═══════════════════════════════════════════════════════════════ */

// ─── API Helper ───
const API = {
  baseURL: '',

  async request(endpoint, options = {}) {
    const tokens = Auth.getTokens();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (tokens && tokens.access) {
      headers['Authorization'] = `Bearer ${tokens.access}`;
    }

    const config = {
      ...options,
      headers,
    };

    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    const response = await fetch(this.baseURL + endpoint, config);
    const data = await response.json();

    if (!response.ok) {
      throw { status: response.status, data };
    }

    return data;
  },

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  },

  post(endpoint, body) {
    return this.request(endpoint, { method: 'POST', body });
  },

  put(endpoint, body) {
    return this.request(endpoint, { method: 'PUT', body });
  },

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  },
};

// ─── Auth Helper ───
const Auth = {
  setTokens(tokens) {
    localStorage.setItem('mz_tokens', JSON.stringify(tokens));
    const verify = localStorage.getItem('mz_tokens');
    console.log('✅ Tokens saved:', verify ? 'SUCCESS' : 'FAILED');
    return !!verify;
  },

  setUser(user) {
    localStorage.setItem('mz_user', JSON.stringify(user));
    const verify = localStorage.getItem('mz_user');
    console.log('✅ User saved:', verify ? 'SUCCESS' : 'FAILED');
    return !!verify;
  },

  getTokens() {
    try {
      const data = localStorage.getItem('mz_tokens');
      return data ? JSON.parse(data) : null;
    } catch {
      return null;
    }
  },

  getUser() {
    try {
      const data = localStorage.getItem('mz_user');
      return data ? JSON.parse(data) : null;
    } catch {
      return null;
    }
  },

  isLoggedIn() {
    const tokens = this.getTokens();
    const hasToken = !!(tokens && tokens.access);
    console.log('🔍 isLoggedIn check:', hasToken ? 'YES' : 'NO');
    return hasToken;
  },

  saveAuthAndRedirect(tokens, user, url = '/dashboard/') {
    console.log('💾 Saving auth data...');
    const tokensSaved = this.setTokens(tokens);
    const userSaved = this.setUser(user);

    if (!tokensSaved || !userSaved) {
      console.error('❌ Failed to save auth data!');
      Toast.error('Error', 'Login failed - could not save session.');
      return;
    }

    console.log('✅ Auth saved, redirecting to:', url);
    setTimeout(() => window.location.replace(url), 100);
  },

  logout() {
    localStorage.removeItem('mz_tokens');
    localStorage.removeItem('mz_user');
    window.location.replace('/login/');
  },
};

// ─── Toast Notifications ───
const Toast = {
  container: null,

  init() {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
  },

  show(title, message, type = 'info') {
    this.init();

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icons = {
      success: '✓',
      error: '✕',
      warning: '⚠',
      info: 'ℹ',
    };

    toast.innerHTML = `
      <div class="toast-icon">${icons[type] || icons.info}</div>
      <div class="toast-content">
        <div class="toast-title">${title}</div>
        <div class="toast-message">${message}</div>
      </div>
    `;

    this.container.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'slideIn 0.3s ease reverse';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  },

  success(title, message) {
    this.show(title, message, 'success');
  },

  error(title, message) {
    this.show(title, message, 'error');
  },

  warning(title, message) {
    this.show(title, message, 'warning');
  },

  info(title, message) {
    this.show(title, message, 'info');
  },
};

// ─── Modal Helper ───
const Modal = {
  show(title, content, actions = '') {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">${title}</h2>
          <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
        </div>
        <div class="modal-body">${content}</div>
        ${actions ? `<div class="modal-actions" style="margin-top: 1.5rem; display: flex; gap: 0.75rem;">${actions}</div>` : ''}
      </div>
    `;

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) overlay.remove();
    });

    document.body.appendChild(overlay);
    return overlay;
  },

  close() {
    const overlay = document.querySelector('.modal-overlay');
    if (overlay) overlay.remove();
  },
};

// ─── Utility Functions ───
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
  }).format(amount);
}

function formatNumber(num) {
  return new Intl.NumberFormat('en-IN').format(num);
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

function formatDateTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function setLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner"></span> Loading...';
  } else {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || button.innerHTML;
  }
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ─── Auto-refresh for live prices ───
let priceRefreshInterval = null;

function startPriceRefresh(callback, interval = 10000) {
  if (priceRefreshInterval) {
    clearInterval(priceRefreshInterval);
  }
  priceRefreshInterval = setInterval(callback, interval);
}

function stopPriceRefresh() {
  if (priceRefreshInterval) {
    clearInterval(priceRefreshInterval);
    priceRefreshInterval = null;
  }
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  stopPriceRefresh();
});
