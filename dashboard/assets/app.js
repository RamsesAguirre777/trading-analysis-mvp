/**
 * Trading Dashboard - Dynamic Data Integration
 * Integrates with latest_analysis.json from n8n workflow
 */

class TradingDashboard {
    constructor() {
        this.chart = null;
        this.currentMarketType = 'stocks';
        this.analysisData = null;
        this.manualLevels = {
            breakPoint: null,
            maxPosExp: null,
            intPosExp: null,
            intNegExp: null,
            maxNegExp: null
        };
        this.fallbackData = this.createFallbackData();
        this.isOffline = false;
        
        // Auto-refresh settings
        this.refreshInterval = 30000; // 30 seconds
        this.refreshTimer = null;
        
        this.init();
    }
    
    async init() {
        console.log('🚀 Initializing Trading Dashboard...');
        
        // Initialize chart
        this.initChart();
        
        // Load initial data
        await this.loadAnalysisData();
        
        // Set up auto-refresh
        this.startAutoRefresh();
        
        // Set up event listeners
        this.setupEventListeners();
        
        console.log('✅ Dashboard initialized successfully');
    }
    
    async loadAnalysisData() {
        try {
            console.log('📡 Loading analysis data...');
            
            const response = await fetch('./data/latest_analysis.json', {
                cache: 'no-cache',
                headers: {
                    'Cache-Control': 'no-cache'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const analysis = await response.json();
            
            // Validate data structure
            if (!this.validateAnalysisData(analysis)) {
                throw new Error('Invalid analysis data structure');
            }
            
            this.analysisData = analysis;
            this.isOffline = false;
            
            // Update all dashboard components
            this.updateDashboardData(analysis);
            this.updateChart(analysis);
            this.updateAlerts(analysis);
            
            console.log(`✅ Analysis data loaded for ${analysis.symbol}`);
            this.updateLastRefreshTime();
            
        } catch (error) {
            console.error('❌ Error loading analysis data:', error);
            this.handleDataLoadError(error);
        }
    }
    
    validateAnalysisData(data) {
        const requiredFields = [
            'symbol',
            'analysis_timestamp',
            'gap_analysis',
            'trading_signals'
        ];
        
        return requiredFields.every(field => field in data);
    }
    
    handleDataLoadError(error) {
        console.log('🔄 Falling back to cached/example data...');
        this.isOffline = true;
        
        // Use last known data or fallback
        const dataToUse = this.analysisData || this.fallbackData;
        
        this.updateDashboardData(dataToUse);
        this.updateChart(dataToUse);
        this.updateAlerts(dataToUse);
        
        // Show offline indicator
        this.showOfflineIndicator(error.message);
    }
    
    updateDashboardData(analysis) {
        try {
            // Update symbol and basic info
            const symbolElement = document.getElementById('symbolName');
            if (symbolElement) {
                symbolElement.textContent = analysis.symbol || 'UNKNOWN';
                if (this.isOffline) {
                    symbolElement.textContent += ' (OFFLINE)';
                    symbolElement.style.color = '#ff4444';
                } else {
                    symbolElement.style.color = '#00ff00';
                }
            }
            
            // Update current price
            const currentPrice = analysis.current_day?.current_price || 
                               analysis.trading_signals?.entry_levels?.[0] || 
                               0;
            document.getElementById('currentPrice').textContent = `$${currentPrice.toFixed(2)}`;
            
            // Update Gap Analysis
            this.updateGapAnalysis(analysis.gap_analysis);
            
            // Update Previous Day Data
            this.updatePreviousDayData(analysis.previous_day);
            
            // Update Current Day Data
            this.updateCurrentDayData(analysis.current_day);
            
            // Update EMAs
            this.updateEMAs(analysis.emas_1h);
            
            // Update Bollinger Bands
            this.updateBollingerBands(analysis.bollinger_bands);
            
            // Update Trading Signals (in alerts section)
            this.updateTradingSignalsDisplay(analysis.trading_signals);
            
        } catch (error) {
            console.error('Error updating dashboard data:', error);
        }
    }
    
    updateGapAnalysis(gapAnalysis) {
        if (!gapAnalysis) return;
        
        const gapDirection = gapAnalysis.gap_direction || 'unknown';
        const gapSize = gapAnalysis.gap_size || 0;
        const gapPercentage = gapAnalysis.gap_percentage || 0;
        const fillProbability = gapAnalysis.fill_probability || 0;
        const classification = gapAnalysis.classification || 'unknown';
        
        // Update gap size with color
        const gapSizeElement = document.getElementById('gapSize');
        if (gapSizeElement) {
            const gapText = `${gapDirection === 'up' ? '+' : ''}${gapSize.toFixed(2)} (${gapPercentage >= 0 ? '+' : ''}${gapPercentage.toFixed(1)}%)`;
            gapSizeElement.textContent = gapText;
            gapSizeElement.className = gapDirection === 'up' ? 'gap-positive' : 'gap-negative';
        }
        
        // Update gap type
        const gapTypeElement = document.getElementById('gapType');
        if (gapTypeElement) {
            const typeEmoji = classification === 'large' ? '🔴' : 
                            classification === 'medium' ? '🟡' : '🟢';
            gapTypeElement.textContent = `${classification.toUpperCase()} GAP ${typeEmoji}`;
        }
    }
    
    updatePreviousDayData(previousDay) {
        if (!previousDay) return;
        
        const prevElements = {
            'prevClose': previousDay.close
        };
        
        Object.entries(prevElements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element && value !== undefined) {
                element.textContent = value.toFixed(2);
            }
        });
    }
    
    updateCurrentDayData(currentDay) {
        if (!currentDay) return;
        
        const elements = {
            'dayHigh': currentDay.high,
            'dayLow': currentDay.low,
            'gapCurrentPrice': currentDay.current_price
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element && value !== undefined) {
                element.textContent = value.toFixed(2);
            }
        });
    }
    
    updateEMAs(emas) {
        if (!emas) return;
        
        // Update data display
        const emaElements = document.querySelectorAll('#emas .data-row .level-value');
        if (emaElements.length >= 3) {
            emaElements[0].textContent = (emas.ema20 || 0).toFixed(2);
            emaElements[1].textContent = (emas.ema50 || 0).toFixed(2);
            emaElements[2].textContent = (emas.ema200 || 0).toFixed(2);
        }
    }
    
    updateBollingerBands(bollingerBands) {
        if (!bollingerBands) return;
        
        const bbElements = document.querySelectorAll('#bollinger .data-row .level-value');
        if (bbElements.length >= 4) {
            bbElements[0].textContent = (bollingerBands.premarket_bbt_1h || 0).toFixed(2);
            bbElements[1].textContent = (bollingerBands.premarket_bbb_1h || 0).toFixed(2);
            bbElements[2].textContent = (bollingerBands.market_close_bbt_1h || 0).toFixed(2);
            bbElements[3].textContent = (bollingerBands.market_close_bbb_1h || 0).toFixed(2);
        }
    }
    
    updateTradingSignalsDisplay(tradingSignals) {
        if (!tradingSignals) return;
        
        // Add trading signal info to alerts section if not already there
        const alertsSection = document.querySelector('.alerts-section');
        if (alertsSection) {
            // Remove existing trading signal alert
            const existingSignal = alertsSection.querySelector('.trading-signal-alert');
            if (existingSignal) {
                existingSignal.remove();
            }
            
            // Add new trading signal alert
            const signalAlert = document.createElement('div');
            signalAlert.className = `alert ${tradingSignals.primary_direction === 'LONG' ? 'alert-warning' : 'alert-caution'} trading-signal-alert`;
            signalAlert.innerHTML = `
                📊 ${tradingSignals.primary_direction} Signal - 
                Confidence: ${(tradingSignals.confidence * 100).toFixed(0)}% - 
                R/R: ${tradingSignals.risk_reward || 'N/A'}:1
            `;
            alertsSection.appendChild(signalAlert);
        }
    }
    
    updateChart(analysis) {
        if (!this.chart || !analysis) return;
        
        try {
            const currentPrice = analysis.current_day?.current_price || 0;
            const dayHigh = analysis.current_day?.high || currentPrice * 1.01;
            const dayLow = analysis.current_day?.low || currentPrice * 0.99;
            
            // Prepare levels for chart
            const levels = [
                { 
                    value: analysis.bollinger_bands?.premarket_bbt_1h || currentPrice * 1.05, 
                    label: 'BBT 1H', 
                    color: '#000000', 
                    borderDash: [5, 5] 
                },
                { 
                    value: dayHigh, 
                    label: 'Day High', 
                    color: '#ffffff', 
                    borderDash: [] 
                },
                { 
                    value: currentPrice, 
                    label: 'CURRENT PRICE', 
                    color: '#00ff00', 
                    borderDash: [], 
                    borderWidth: 3 
                },
                { 
                    value: dayLow, 
                    label: 'Day Low', 
                    color: '#ffffff', 
                    borderDash: [] 
                },
                { 
                    value: analysis.emas_1h?.ema20 || currentPrice * 0.98, 
                    label: 'EMA20 1H', 
                    color: '#000000', 
                    borderDash: [5, 5] 
                },
                { 
                    value: analysis.emas_1h?.ema50 || currentPrice * 0.96, 
                    label: 'EMA50 1H', 
                    color: '#ff8800', 
                    borderDash: [5, 5] 
                },
                { 
                    value: analysis.bollinger_bands?.premarket_bbb_1h || currentPrice * 0.90, 
                    label: 'BBB 1H', 
                    color: '#000000', 
                    borderDash: [5, 5] 
                },
                { 
                    value: analysis.emas_1h?.ema200 || currentPrice * 0.85, 
                    label: 'EMA200 1H', 
                    color: '#88ff00', 
                    borderDash: [5, 5] 
                }
            ];
            
            // Add manual levels if they exist
            Object.entries(this.manualLevels).forEach(([key, value]) => {
                if (value) {
                    const colors = {
                        breakPoint: '#ff00ff',
                        maxPosExp: '#ff4444',
                        intPosExp: '#ff8888',
                        intNegExp: '#8888ff',
                        maxNegExp: '#4444ff'
                    };
                    
                    levels.push({
                        value: value,
                        label: key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase()),
                        color: colors[key] || '#ffffff',
                        borderDash: []
                    });
                }
            });
            
            this.updateHorizontalLines(levels);
            
            // Update Y-axis range based on current data
            const minPrice = Math.min(...levels.map(l => l.value)) * 0.95;
            const maxPrice = Math.max(...levels.map(l => l.value)) * 1.05;
            
            this.chart.options.scales.y.min = minPrice;
            this.chart.options.scales.y.max = maxPrice;
            
            // Update chart data with some price movement simulation
            this.updateChartData(currentPrice);
            
        } catch (error) {
            console.error('Error updating chart:', error);
        }
    }
    
    updateHorizontalLines(levels) {
        if (!this.chart) return;
        
        // Clear existing annotations
        if (this.chart.options.plugins.annotation) {
            this.chart.options.plugins.annotation.annotations = {};
        }
        
        const annotations = {};
        
        levels.forEach((level, index) => {
            if (level.value && !isNaN(level.value)) {
                annotations[`line${index}`] = {
                    type: 'line',
                    yMin: level.value,
                    yMax: level.value,
                    borderColor: level.color,
                    borderWidth: level.borderWidth || 2,
                    borderDash: level.borderDash || [],
                    label: {
                        content: `${level.label}: ${level.value.toFixed(2)}`,
                        enabled: true,
                        position: 'end',
                        backgroundColor: level.color,
                        color: level.color === '#000000' ? '#ffffff' : '#000000',
                        font: {
                            size: 10
                        }
                    }
                };
            }
        });
        
        this.chart.options.plugins.annotation = { annotations };
        this.chart.update('none');
    }
    
    updateChartData(basePrice) {
        if (!this.chart || !basePrice) return;
        
        const chartData = this.chart.data.datasets[0].data;
        
        // Add new data point with small random variation
        const variation = (Math.random() - 0.5) * (basePrice * 0.005); // 0.5% variation
        const newPrice = basePrice + variation;
        
        chartData.shift();
        chartData.push(newPrice);
        
        this.chart.update('none');
    }
    
    updateAlerts(analysis) {
        if (!analysis) return;
        
        const alertsContainer = document.querySelector('.alerts-section');
        if (!alertsContainer) return;
        
        // Clear existing alerts but keep the header
        alertsContainer.innerHTML = '<h3>🚨 ALERTS</h3>';
        
        // Gap fill alerts
        if (analysis.gap_analysis?.fill_probability > 0.7) {
            this.addAlert(alertsContainer, 'alert-caution', 
                `GAP FILL probability: ${(analysis.gap_analysis.fill_probability * 100).toFixed(0)}%`);
        }
        
        // Overbought/oversold alerts
        if (analysis.alerts?.overbought_1h) {
            this.addAlert(alertsContainer, 'alert-caution', 'CAUTION: Price outside BBT 1H');
        }
        
        if (analysis.alerts?.correction_level && analysis.alerts.correction_level !== 'none') {
            const correctionText = `${analysis.alerts.correction_level} correction expected`;
            this.addAlert(alertsContainer, 'alert-warning', correctionText);
        }
        
        // Trading signal alert (already handled in updateTradingSignalsDisplay)
        
        // Offline alert
        if (this.isOffline) {
            this.addAlert(alertsContainer, 'alert-caution', '📡 OFFLINE - Using cached data');
        }
    }
    
    addAlert(container, className, message) {
        const alert = document.createElement('div');
        alert.className = `alert ${className}`;
        alert.textContent = message;
        container.appendChild(alert);
    }
    
    showOfflineIndicator(errorMessage) {
        // Update timestamp to show offline status
        this.updateLastRefreshTime(`OFFLINE: ${errorMessage}`);
    }
    
    updateLastRefreshTime(customMessage = null) {
        let timestampElement = document.getElementById('lastRefresh');
        
        if (!timestampElement) {
            // Create timestamp element if it doesn't exist
            timestampElement = document.createElement('div');
            timestampElement.id = 'lastRefresh';
            timestampElement.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(0, 0, 0, 0.8);
                color: #ffffff;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 1000;
            `;
            document.body.appendChild(timestampElement);
        }
        
        const timestamp = customMessage || `Last updated: ${new Date().toLocaleTimeString()}`;
        timestampElement.textContent = timestamp;
        timestampElement.style.color = customMessage ? '#ff4444' : '#00ff00';
    }
    
    initChart() {
        const ctx = document.getElementById('tradingChart');
        if (!ctx) {
            console.error('Chart canvas not found');
            return;
        }
        
        this.chart = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: Array.from({length: 100}, (_, i) => i),
                datasets: [{
                    label: 'Price',
                    data: Array.from({length: 100}, () => 170 + (Math.random() - 0.5) * 4),
                    borderColor: '#ffffff',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    annotation: {
                        annotations: {}
                    }
                },
                scales: {
                    x: {
                        display: false
                    },
                    y: {
                        beginAtZero: false,
                        min: 150,
                        max: 180,
                        grid: {
                            color: '#333'
                        },
                        ticks: {
                            color: '#ffffff',
                            callback: function(value) {
                                return '$' + value.toFixed(2);
                            }
                        }
                    }
                },
                animation: {
                    duration: 0
                }
            }
        });
    }
    
    startAutoRefresh() {
        // Clear any existing timer
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        
        // Set up new timer
        this.refreshTimer = setInterval(() => {
            console.log('🔄 Auto-refreshing dashboard data...');
            this.loadAnalysisData();
        }, this.refreshInterval);
        
        console.log(`⏰ Auto-refresh enabled (${this.refreshInterval/1000}s interval)`);
    }
    
    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
            console.log('⏹️ Auto-refresh stopped');
        }
    }
    
    setupEventListeners() {
        // Manual refresh button (create if doesn't exist)
        let refreshBtn = document.getElementById('refreshBtn');
        if (!refreshBtn) {
            refreshBtn = document.createElement('button');
            refreshBtn.id = 'refreshBtn';
            refreshBtn.textContent = '🔄 Refresh';
            refreshBtn.style.cssText = `
                position: fixed;
                top: 50px;
                right: 10px;
                background: #00ff00;
                color: #000;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                z-index: 1000;
            `;
            document.body.appendChild(refreshBtn);
        }
        
        refreshBtn.addEventListener('click', () => {
            console.log('🔄 Manual refresh triggered');
            this.loadAnalysisData();
        });
        
        // Update manual levels function
        window.updateManualLevels = () => {
            this.manualLevels.breakPoint = parseFloat(document.getElementById('breakPoint').value) || null;
            this.manualLevels.maxPosExp = parseFloat(document.getElementById('maxPosExp').value) || null;
            this.manualLevels.intPosExp = parseFloat(document.getElementById('intPosExp').value) || null;
            this.manualLevels.intNegExp = parseFloat(document.getElementById('intNegExp').value) || null;
            this.manualLevels.maxNegExp = parseFloat(document.getElementById('maxNegExp').value) || null;
            
            // Update chart with new levels
            if (this.analysisData) {
                this.updateChart(this.analysisData);
            }
            
            console.log('📊 Manual levels updated', this.manualLevels);
        };
        
        // Window focus event for immediate refresh
        window.addEventListener('focus', () => {
            console.log('👁️ Window focused - refreshing data');
            this.loadAnalysisData();
        });
        
        // Page visibility API for better performance
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.startAutoRefresh();
                this.loadAnalysisData();
            } else {
                this.stopAutoRefresh();
            }
        });
    }
    
    createFallbackData() {
        return {
            symbol: "NVDA",
            analysis_timestamp: new Date().toISOString(),
            gap_analysis: {
                gap_size: 8.02,
                gap_direction: "up",
                gap_percentage: 4.9,
                fill_probability: 0.85,
                classification: "large"
            },
            imbalance_analysis: {
                bbt_ratio: 1.047,
                bbb_ratio: 0.994,
                imbalance_direction: "bullish",
                strength: "moderate"
            },
            trend_analysis: {
                short_term: "bullish",
                medium_term: "bullish",
                long_term: "bullish",
                trend_strength: 1.0
            },
            alerts: {
                overbought_1m: true,
                overbought_5m: true,
                overbought_30m: true,
                overbought_1h: true,
                correction_level: "high"
            },
            directional_targets: {
                bullish_target: 172.81,
                bearish_target: 169.91,
                first_target_prediction: "bullish"
            },
            trading_signals: {
                primary_direction: "SHORT",
                confidence: 0.73,
                entry_levels: [171.50, 171.00],
                stop_loss: 173.00,
                take_profit: [169.91, 168.50],
                risk_reward: 0.8
            },
            previous_day: {
                high: 165.49,
                low: 162.02,
                close: 163.87,
                change: 3.47
            },
            current_day: {
                high: 172.81,
                low: 169.91,
                current_price: 171.89,
                change: 2.90
            },
            bollinger_bands: {
                premarket_bbt_1h: 174.54,
                premarket_bbb_1h: 160.82,
                market_close_bbt_1h: 166.74,
                market_close_bbb_1h: 161.84
            },
            emas_1h: {
                ema20: 167.68,
                ema50: 164.25,
                ema200: 152.47
            }
        };
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.tradingDashboard = new TradingDashboard();
});