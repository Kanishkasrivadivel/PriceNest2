// =====================================================
// ALERTS PAGE - INITIALIZATION
// =====================================================

document.addEventListener('DOMContentLoaded', function () {
  // Check authentication
  if (!isLoggedIn()) {
    window.location.href = 'login.html';
    return;
  }

  // Update navigation
  updateNavigation();

  // Load alerts
  loadAlerts();
});

// =====================================================
// NAVIGATION UPDATE
// =====================================================

function updateNavigation() {
  const navButtons = document.getElementById('navButtons');
  const userData = getUserData();
  const firstName = userData.firstName || 'User';
  const alertsCount = getAlerts().length;
  const wishlistCount = getWishlist().length;

  navButtons.innerHTML = `
    <button class="nav-icon-btn" onclick="window.location.href='alerts.html'" title="Alerts">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
      </svg>
      ${alertsCount > 0 ? `<span class="badge">${alertsCount}</span>` : ''}
    </button>
    
    <button class="nav-icon-btn" onclick="window.location.href='wishlist.html'" title="Wishlist">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>
      ${wishlistCount > 0 ? `<span class="badge">${wishlistCount}</span>` : ''}
    </button>
    
    <button class="btn primary" onclick="window.location.href='profile.html'">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
      ${firstName}
    </button>
  `;
}

// =====================================================
// LOAD AND DISPLAY ALERTS
// =====================================================

function loadAlerts() {
  const container = document.getElementById('alertsContainer');
  const alerts = getAlerts();

  if (alerts.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
        </div>
        <div class="empty-state-title">No alerts yet</div>
        <div class="empty-state-text">
          Create price alerts to get notified when products reach your target price
        </div>
        <button class="btn primary" onclick="window.location.href='index.html'">
          Start Searching
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="alerts-grid">
      ${alerts.map(alert => createAlertCard(alert)).join('')}
    </div>
  `;
}

function createAlertCard(alert) {
  return `
    <div class="alert-card">
      <div class="alert-info">
        <div class="alert-product">${alert.product}</div>
        <div class="alert-details">
          <div class="alert-detail">
            <div class="alert-detail-label">Target Price</div>
            <div class="alert-detail-value price">${formatCurrency(alert.targetPrice)}</div>
          </div>
          <div class="alert-detail">
            <div class="alert-detail-label">Created</div>
            <div class="alert-detail-value">${formatDate(alert.createdAt)}</div>
          </div>
        </div>
        <div class="alert-status ${alert.active ? 'active' : 'inactive'}">
          <span class="alert-status-dot"></span>
          ${alert.active ? 'Active' : 'Inactive'}
        </div>
      </div>
      
      <div class="alert-actions">
        <button onclick="toggleAlertStatus('${alert.id}')" title="${alert.active ? 'Deactivate' : 'Activate'}">
          ${alert.active ? `
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 1l22 22"></path>
              <path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"></path>
              <path d="M17 17H3s3-2 3-9"></path>
              <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path>
            </svg>
          ` : `
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          `}
        </button>
        <button class="delete" onclick="handleDeleteAlert('${alert.id}')" title="Delete">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>
  `;
}

// =====================================================
// ALERT ACTIONS
// =====================================================

function toggleAlertStatus(alertId) {
  const alerts = getAlerts();
  const alert = alerts.find(a => a.id === alertId);

  if (alert) {
    alert.active = !alert.active;
    saveAlerts(alerts);
    showNotification(
      `Alert ${alert.active ? 'activated' : 'deactivated'}`,
      alert.active ? 'success' : 'info'
    );
    loadAlerts();
    updateNavigation();
  }
}

function handleDeleteAlert(alertId) {
  if (confirm('Are you sure you want to delete this alert?')) {
    deleteAlert(alertId);
    showNotification('Alert deleted', 'success');
    loadAlerts();
    updateNavigation();
  }
}
