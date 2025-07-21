# Telegram Bot Setup Guide for Trading Analysis MVP

## 🤖 Creating Your Telegram Bot

### Step 1: Create Bot with BotFather
1. Open Telegram and search for `@BotFather`
2. Start conversation with `/start`
3. Create new bot with `/newbot`
4. Choose name: `Trading Analysis Bot`
5. Choose username: `YourTradingAnalysisBot` (must end with 'bot')
6. Save the **Bot Token** provided

### Step 2: Get Your Chat ID
1. Start conversation with your new bot
2. Send any message to your bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your `chat_id` in the response JSON
5. Save this **Chat ID**

### Step 3: Configure N8N Credentials
1. In N8N interface, go to **Credentials**
2. Add new **Telegram Bot** credential
3. Enter your Bot Token
4. Test the connection

## 📱 Bot Commands Structure

### Manual Analysis Commands:
```
/analyze NVDA
/analyze TSLA
/analyze AAPL manual_break_point=171.67
```

### Status Commands:
```
/status - Get last analysis results
/help - Show available commands
/symbols - List supported symbols
```

### Configuration Commands:
```
/set_alerts on/off - Enable/disable alerts
/set_symbols NVDA,TSLA,AAPL - Set watchlist
```

## 🔧 N8N Telegram Integration

### Telegram Trigger Node (Optional)
```json
{
  "parameters": {
    "updates": ["message"],
    "chatId": "{{ $credentials.telegramBot.chatId }}"
  },
  "name": "Telegram Command Trigger",
  "type": "n8n-nodes-base.telegramTrigger"
}
```

### Telegram Send Node Configuration
```json
{
  "parameters": {
    "chatId": "{{ $credentials.telegramBot.chatId }}",
    "text": "={{ $json.message }}",
    "additionalFields": {
      "parse_mode": "Markdown",
      "disable_web_page_preview": true
    }
  },
  "name": "Send Telegram Alert",
  "type": "n8n-nodes-base.telegram"
}
```

## 📊 Message Templates

### Trading Signal Alert Template:
```
🎯 TRADING SIGNAL: NVDA

📈 Direction: LONG
📊 Confidence: 73.5%
💰 Entry: 171.50, 171.00
🛑 Stop Loss: 173.00
🎯 Take Profit: 169.91, 166.51
📋 Risk/Reward: 0.8:1

📊 ANALYSIS:
⬆️ Gap: up 8.02 (4.9%)
📈 Trend: bullish (100%)
⚠️ Alerts: high correction expected
🎯 Target: bearish

⏰ 2025-07-21 09:30:00
```

### Error Alert Template:
```
🚨 TRADING ANALYSIS ERROR

Symbol: NVDA
Error: API timeout
Retry: 2/3

⏰ 2025-07-21 09:30:00
```

### Status Update Template:
```
✅ SYSTEM STATUS

Last Analysis: NVDA (09:30:00)
Active Alerts: 3
API Status: ✅ Connected
Dashboard: ✅ Updated

Watchlist: NVDA, TSLA, AAPL, MSFT
```

## 🔐 Security Configuration

### Environment Variables:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
TELEGRAM_ALERTS_ENABLED=true
TELEGRAM_MAX_MESSAGE_LENGTH=4000
```

### N8N Credential Fields:
- **Bot Token**: Your Telegram bot token
- **Chat ID**: Your personal chat ID
- **Webhook URL**: (Optional) For webhook-based triggers

## 🧪 Testing Your Setup

### Test Message:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "<YOUR_CHAT_ID>",
    "text": "🧪 Test message from Trading Analysis MVP"
  }'
```

### Test N8N Integration:
1. Activate your workflow in N8N
2. Trigger webhook: `POST http://localhost:5678/webhook/trading`
3. Check Telegram for alert message
4. Verify dashboard data is updated

## 📱 Advanced Features

### Rich Message Formatting:
- Use **Markdown** for bold text
- Use `code blocks` for data
- Use emojis for visual appeal
- Include timestamps and symbols

### Error Handling:
- Retry failed message sends
- Fallback to simplified messages if formatting fails
- Log all Telegram interactions

### Rate Limiting:
- Max 20 messages per minute
- Queue messages during high activity
- Batch similar alerts when possible

## 🚀 Production Deployment

1. **Security**: Never commit bot tokens to Git
2. **Monitoring**: Set up alerts for bot failures
3. **Backup**: Configure multiple chat IDs for redundancy
4. **Scaling**: Consider broadcast lists for multiple users