/**
 * Cryptex Insight Engine - Frontend Logic
 * Handles API calls, DOM updates, and interactive elements
 */

const API_BASE = '/api';
const UPDATE_INTERVAL = 5000; // 5 seconds

// ==========================================
// STATE MANAGEMENT
// ==========================================

let appState = {
    connected: false,
    report: null,
    lastUpdate: null
};

// ==========================================
// INITIALIZATION
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Cryptex Insight Engine initializing...');
    initializeApp();
    updateClock();
    setInterval(updateClock, 1000);
});

async function initializeApp() {
    try {
        // Load initial data
        await fetchMarketPulse();
        await fetchFullReport();
        
        // Update UI
        updateNodeMonitor();
        updateDashboard();
        
        appState.connected = true;
        updateConnectionStatus();
        
        console.log('✅ Cryptex Insight Engine online');
    } catch (error) {
        console.error('❌ Initialization error:', error);
        updateConnectionStatus(false);
    }
}

// ==========================================
// API CALLS
// ==========================================

async function fetchMarketPulse() {
    try {
        const response = await fetch(`${API_BASE}/market-pulse`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        appState.report = await response.json();
        appState.lastUpdate = new Date();
        return appState.report;
    } catch (error) {
        console.error('Error fetching market pulse:', error);
        throw error;
    }
}

async function fetchFullReport() {
    try {
        const response = await fetch(`${API_BASE}/full-report`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching full report:', error);
        throw error;
    }
}

async function fetchVisual(filename) {
    return `${API_BASE}/visuals/${filename}`;
}

// ==========================================
// DOM UPDATE FUNCTIONS
// ==========================================

function updateConnectionStatus(connected = true) {
    const statusText = document.getElementById('status-text');
    const statusDiv = document.querySelector('.status-indicator');
    
    if (connected) {
        statusText.textContent = 'CONNECTED';
        statusText.style.color = '#39ff14';
        statusDiv.classList.remove('offline');
    } else {
        statusText.textContent = 'OFFLINE';
        statusText.style.color = '#ff003c';
        statusDiv.classList.add('offline');
    }
}

function updateNodeMonitor() {
    const pulse = appState.report;
    if (!pulse) return;
    
    // Update header metrics
    document.getElementById('total-liquidity').textContent = 
        formatCurrency(pulse.market_metrics?.total_liquidity || 0);
    
    document.getElementById('total-orders').textContent = 
        (pulse.market_metrics?.total_orders || 0).toLocaleString();
    
    document.getElementById('success-rate').textContent = 
        (pulse.market_metrics?.success_rate || 0).toFixed(2) + '%';
    
    // Update node info
    document.getElementById('node-id').textContent = 
        `NODE: ${pulse.node_id || 'UNKNOWN'}`;
    
    if (pulse.timestamp) {
        document.getElementById('timestamp').textContent = 
            `TIME: ${new Date(pulse.timestamp).toLocaleTimeString()}`;
    }
}

function updateDashboard() {
    const pulse = appState.report;
    if (!pulse) return;
    
    // Update executive summary
    const insights = pulse.insights || {};
    
    document.getElementById('peak-hour').textContent = 
        `${insights.peak_ordering_hour || '--'}:00`;
    
    document.getElementById('fastest-zone').textContent = 
        insights.fastest_delivery_zone || '--';
    
    document.getElementById('pop-payment').textContent = 
        insights.most_popular_payment || '--';
    
    document.getElementById('avg-items').textContent = 
        (insights.avg_items_per_order || 0).toFixed(2);
    
    document.getElementById('top-vendor').textContent = 
        insights.top_restaurant || '--';
    
    document.getElementById('volatility').textContent = 
        (insights.volatility_index || 0).toFixed(3);
    
    // Update statistics panels
    updateStatsPanel();
    
    // Load visualization images
    loadVisualizations();
}

function updateStatsPanel() {
    const pulse = appState.report;
    if (!pulse) return;
    
    const stats = pulse.market_metrics?.stats?.order_amount || {};
    const delivery = pulse.market_metrics?.stats?.delivery_time || {};
    const quantity = pulse.market_metrics?.stats?.quantity || {};
    const orderHour = pulse.market_metrics?.stats?.order_hour || {};
    const metrics = pulse.market_metrics || {};
    const metadata = pulse.metadata || {};
    
    // Order metrics
    document.getElementById('stat-avg-order').textContent = 
        formatCurrency(stats.mean || 0);
    
    document.getElementById('stat-median-order').textContent = 
        formatCurrency(stats.median || 0);
    
    document.getElementById('stat-std-order').textContent = 
        '₹' + (stats.std || 0).toFixed(2);
    
    document.getElementById('stat-min-order').textContent = 
        formatCurrency(stats.min || 0);
    
    document.getElementById('stat-max-order').textContent = 
        formatCurrency(stats.max || 0);
    
    // Delivery metrics
    document.getElementById('stat-avg-delivery').textContent = 
        (delivery.mean || 0).toFixed(1) + ' min';
    
    document.getElementById('stat-median-delivery').textContent = 
        (delivery.median || 0).toFixed(1) + ' min';
    
    document.getElementById('stat-std-delivery').textContent = 
        (delivery.std || 0).toFixed(1) + ' min';
    
    document.getElementById('stat-min-delivery').textContent = 
        (delivery.min || 0).toFixed(1) + ' min';
    
    document.getElementById('stat-max-delivery').textContent = 
        (delivery.max || 0).toFixed(1) + ' min';
    
    // Order status
    updateStatusTable();
    
    // Feature statistics
    document.getElementById('stat-order-hour').textContent = 
        (orderHour.mean || 0).toFixed(1) + 'h';
    
    document.getElementById('stat-quantity').textContent = 
        (quantity.mean || 0).toFixed(2);
    
    // Metadata stats
    document.getElementById('stat-records').textContent = 
        (metadata.total_records || metrics.total_orders || 0).toLocaleString();
    
    document.getElementById('stat-columns').textContent = 
        (metadata.total_columns || metadata.columns?.length || 0);
    
    // Market intel
    document.getElementById('stat-delivered').textContent = 
        (metrics.successful_deliveries || 0).toLocaleString();
    
    document.getElementById('stat-delayed').textContent = 
        (metrics.delayed_orders || 0).toLocaleString();
    
    document.getElementById('stat-cancelled').textContent = 
        (metrics.cancelled_orders || 0).toLocaleString();
    
    document.getElementById('stat-q25').textContent = 
        formatCurrency(stats.q25 || 0);
    
    document.getElementById('stat-q75').textContent = 
        formatCurrency(stats.q75 || 0);
}

function updateStatusTable() {
    const pulse = appState.report;
    if (!pulse) return;
    
    const statusData = pulse.market_metrics?.stats?.order_status || {};
    const tbody = document.getElementById('status-tbody');
    
    tbody.innerHTML = '';
    
    for (const [status, count] of Object.entries(statusData)) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${status}</td>
            <td>${count.toLocaleString()}</td>
        `;
        tbody.appendChild(tr);
    }
}

async function loadVisualizations() {
    const visualizations = [
        { id: 'img-trends', file: '01_trend_analysis.png' },
        { id: 'img-correlation', file: '02_correlation_heatmap.png' },
        { id: 'img-distribution', file: '03_distribution_outliers.png' },
        { id: 'img-pca', file: '04_pca_analysis.png' },
        { id: 'img-kmeans', file: '05_kmeans_elbow.png' }
    ];
    
    for (const vis of visualizations) {
        try {
            const imgElement = document.getElementById(vis.id);
            if (imgElement) {
                imgElement.src = await fetchVisual(vis.file);
                imgElement.alt = `Visualization: ${vis.file}`;
                imgElement.onload = () => {
                    console.log(`✓ Loaded ${vis.file}`);
                };
                imgElement.onerror = () => {
                    console.warn(`⚠ Failed to load ${vis.file}`);
                    imgElement.style.display = 'none';
                };
            }
        } catch (error) {
            console.error(`Error loading ${vis.file}:`, error);
        }
    }
}

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

function formatCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN', { 
        maximumFractionDigits: 2,
        minimumFractionDigits: 2
    });
}

function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('footer-time').textContent = timeString;
}

function formatNumber(num) {
    return num.toLocaleString('en-IN');
}

// ==========================================
// EVENT LISTENERS
// ==========================================

// Summary card interactions
document.querySelectorAll('.summary-card').forEach(card => {
    card.addEventListener('click', function() {
        this.classList.toggle('active');
    });
    
    card.addEventListener('mouseenter', function() {
        this.style.background = 'rgba(57, 255, 20, 0.1)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.background = 'rgba(57, 255, 20, 0.02)';
    });
});

// Visual panel interactions
document.querySelectorAll('.visual-panel').forEach(panel => {
    panel.addEventListener('click', function() {
        this.classList.toggle('expanded');
    });
});

// ==========================================
// ERROR HANDLING
// ==========================================

window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// ==========================================
// PERIODIC UPDATES
// ==========================================

// Uncomment to enable auto-refresh
/*
setInterval(() => {
    if (appState.connected) {
        fetchMarketPulse().then(() => {
            updateNodeMonitor();
            console.log('🔄 Dashboard updated');
        }).catch(error => {
            console.error('Auto-update failed:', error);
        });
    }
}, UPDATE_INTERVAL);
*/

console.log('✓ Cryptex Insight Engine script loaded');
