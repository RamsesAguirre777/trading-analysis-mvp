# N8N Automation Setup Guide - Trading Analysis MVP

## 🎯 OVERVIEW
Complete automation setup for Trading Analysis MVP using N8N. This workflow orchestrates API data fetching, trading calculator execution, dashboard updates, and Telegram alerts.

## 📋 PREREQUISITES

### Software Requirements:
```bash
# Install N8N globally
npm install -g n8n

# Install Python dependencies (if not done)
pip install -r requirements.txt

# Verify installations
n8n --version
python --version
```

### API Keys Required:
- **Polygon.io API Key** (Recommended) - [Get Free Key](https://polygon.io/)
- **Alpaca API Key** (Alternative) - [Get Free Key](https://alpaca.markets/)
- **Telegram Bot Token** (Optional) - [Create Bot](https://t.me/BotFather)

## 🚀 QUICK SETUP

### Step 1: Start N8N
```bash
# Start N8N server
n8n start

# Access web interface
# Open: http://localhost:5678
```

### Step 2: Import Workflow
1. Copy `n8n/workflows/trading_analysis_workflow.json`
2. In N8N interface: **Import from File**
3. Select the workflow JSON file
4. Click **Import**

### Step 3: Configure Credentials
1. Go to **Credentials** in N8N
2. Add **Polygon API** credential:
   - Name: `polygon-credentials`
   - API Key: `your_polygon_api_key`
3. Add **Telegram Bot** credential:
   - Name: `telegram-credentials`  
   - Bot Token: `your_telegram_bot_token`
   - Chat ID: `your_chat_id`

### Step 4: Update Paths
Edit these nodes with your actual paths:
- **Execute Trading Calculator**: Update `workingDirectory`
- **Save Dashboard Data**: Update file path
- **Environment variables**: Update in `.env` file

## 🔧 DETAILED CONFIGURATION

### Environment Setup:
```bash
# Copy environment template
cp n8n/templates/environment_setup.env .env

# Edit with your values
nano .env
```

### Required Environment Variables:
```env
# Core Paths
TRADING_CALCULATOR_PATH=/full/path/to/trading_calculator.py
DASHBOARD_DATA_PATH=/full/path/to/dashboard/data/
PROJECT_ROOT=/full/path/to/trading-analysis-mvp

# API Configuration
POLYGON_API_KEY=your_polygon_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

## 🎛️ WORKFLOW COMPONENTS

### 1. Triggers:
- **Webhook Trigger**: `POST /webhook/trading`
- **Schedule Trigger**: Daily at 9:25 AM EST
- **Manual Trigger**: Button in N8N interface

### 2. Data Pipeline:
```
Trigger → API Calls → Data Transform → Calculator → Parse Result → Output
```

### 3. Parallel API Calls:
- **Previous Day Data**: Polygon/Alpaca historical
- **Current Price**: Real-time price data
- **Hourly Data**: For EMA calculations

### 4. Output Actions:
- **Save to Dashboard**: `latest_analysis.json`
- **Telegram Alert**: Formatted trading signal
- **Webhook Response**: JSON analysis result

## 🧪 TESTING THE PIPELINE

### Manual Test via Webhook:
```bash
curl -X POST http://localhost:5678/webhook/trading \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "NVDA",
    "manual_break_points": {
      "break_point": 171.67,
      "max_pos_exp": 174.04,
      "int_pos_exp": 172.85,
      "int_neg_exp": 170.48,
      "max_neg_exp": 169.29
    }
  }'
```

### Expected Response:
```json
{
  "analysis_timestamp": "2025-07-21T14:30:00.000Z",
  "symbol": "NVDA",
  "trading_signals": {
    "primary_direction": "SHORT",
    "confidence": 0.73,
    "entry_levels": [171.50, 171.00]
  }
}
```

### Verify Results:
```bash
# Check dashboard data
cat dashboard/data/latest_analysis.json

# Check Telegram delivery (look for message in your chat)

# Check N8N execution logs (in web interface)
```

## 📱 TELEGRAM INTEGRATION

### Bot Commands:
```
/analyze NVDA - Trigger manual analysis
/status - Get system status
/help - Show available commands
```

### Message Format:
```
🎯 TRADING SIGNAL: NVDA

📈 Direction: SHORT
📊 Confidence: 73.5%
💰 Entry: 171.50, 171.00
🛑 Stop Loss: 173.00
🎯 Take Profit: 169.91, 166.51

⏰ 2025-07-21 14:30:00
```

## 🔄 SCHEDULING

### Premarket Analysis (9:25 AM EST):
- Automatically analyzes default symbols
- Sends batch alerts via Telegram
- Updates dashboard with all results

### Custom Schedules:
```javascript
// Every hour during market hours
"25 9-16 * * 1-5"

// Every 15 minutes during active trading
"*/15 9-16 * * 1-5"

// Custom weekend analysis
"0 10 * * 6,0"
```

## 🚨 ERROR HANDLING

### Automatic Retries:
- **API Failures**: 3 retries with exponential backoff
- **Calculator Errors**: 2 retries with fixed delay
- **Telegram Failures**: 3 retries with linear backoff

### Fallback Strategies:
- **API Down**: Switch to alternative API or cached data
- **Calculator Fails**: Return default analysis with error flag
- **Telegram Down**: Log error and continue execution

### Error Notifications:
- Admin alerts for critical failures
- Detailed error logging in N8N
- Fallback analysis when possible

## 📊 MONITORING & MAINTENANCE

### Health Checks:
```bash
# N8N Health
curl http://localhost:5678/healthz

# Webhook Test
curl -X POST http://localhost:5678/webhook/trading \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TEST"}'

# Calculator Direct Test
python src/trading_calculator.py --input data/nvda_test_data.json
```

### Performance Monitoring:
- **Total Execution Time**: < 30 seconds
- **API Response Time**: < 5 seconds  
- **Calculator Execution**: < 3 seconds
- **Dashboard Update**: < 1 second

### Logs Location:
- **N8N Logs**: Available in web interface
- **Calculator Logs**: Console output in N8N
- **Error Logs**: Captured in error handling nodes

## 🔧 TROUBLESHOOTING

### Common Issues:

#### 1. "Command not found: python"
```bash
# Update Execute Command node
Command: python3
# Or use full path
Command: /usr/bin/python3
```

#### 2. "Permission denied"
```bash
chmod +x src/trading_calculator.py
```

#### 3. "API Key Invalid"
- Verify API key in credentials
- Check API key permissions
- Test API key with curl

#### 4. "Telegram message failed"
- Verify bot token and chat ID
- Check bot permissions
- Test with Telegram API directly

#### 5. "Dashboard not updating"
- Check file write permissions
- Verify dashboard directory exists
- Check file path in node configuration

## 🚀 PRODUCTION DEPLOYMENT

### Security:
- Use N8N environment variables for secrets
- Restrict webhook access with authentication
- Monitor API usage and rate limits

### Scaling:
- Use N8N queues for high-volume processing
- Implement caching for repeated API calls
- Consider multiple N8N instances for redundancy

### Backup:
- Export workflow regularly
- Backup credential configurations
- Save environment configurations

## 📈 NEXT STEPS

1. **Test with real API keys**
2. **Configure Telegram bot**
3. **Set up production scheduling**
4. **Monitor performance and errors**
5. **Optimize based on usage patterns**

---

## ✅ SUCCESS CRITERIA

- ✅ Webhook responds in < 30 seconds
- ✅ Dashboard updates with analysis
- ✅ Telegram alerts delivered
- ✅ No errors in N8N execution log
- ✅ Analysis format matches specification

**Ready for production trading analysis automation!** 🚀