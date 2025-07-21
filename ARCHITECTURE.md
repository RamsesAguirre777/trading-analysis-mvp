# 🏗️ Architecture Overview

## System Architecture

```mermaid
graph TB
    A[User Input] --> B[Trading Calculator]
    B --> C[7 Algorithms Engine]
    C --> D[Decision Engine]
    D --> E[JSON Output]
    
    F[N8N Trigger] --> G[Data Fetcher]
    G --> H[API Sources]
    H --> I[Data Transform]
    I --> B
    E --> J[File Writer]
    E --> K[Telegram Alert]
    
    L[Dashboard] --> M[JSON Reader]
    M --> J
    M --> N[Chart Renderer]
    N --> O[Real-time UI]
```

## 🧮 Algorithm Engine Details

### 1. Gap Analysis Engine
```python
def calculate_gap(previous_close: float, current_price: float) -> dict:
    """
    Calculates gap size, direction and fill probability
    
    Classification:
    - Small: <1% gap
    - Medium: 1-3% gap  
    - Large: >3% gap (high fill probability)
    """
```

### 2. Bollinger Bands Imbalance
```python
def analyze_bb_imbalance(premarket_bb: dict, market_close_bb: dict) -> dict:
    """
    Compares BBT/BBB levels between sessions
    
    Ratios:
    - BBT Ratio = premarket_bbt / market_close_bbt
    - BBB Ratio = premarket_bbb / market_close_bbb
    - Imbalance strength based on ratio deviation
    """
```

### 3. EMA Trend Analysis
```python
def analyze_ema_trend(ema20: float, ema50: float, ema200: float, price: float) -> dict:
    """
    Multi-timeframe trend analysis
    
    Trend Rules:
    - Bullish: EMA20 > EMA50 > EMA200 and Price > EMA20
    - Bearish: EMA20 < EMA50 < EMA200 and Price < EMA20
    - Neutral: Mixed conditions
    """
```

## 📊 Data Flow

### Input Processing
1. **JSON Validation**: Schema validation for all input data
2. **Data Sanitization**: Clean and normalize market data
3. **Error Handling**: Graceful handling of missing/invalid data

### Algorithm Execution
1. **Parallel Processing**: Algorithms run independently
2. **Result Aggregation**: Combine all algorithm outputs
3. **Confidence Scoring**: Weight algorithms by historical accuracy

### Output Generation
1. **Signal Generation**: Primary direction with confidence
2. **Risk Management**: Stop loss and take profit calculation
3. **JSON Formatting**: Standardized output structure

## 🔄 N8N Workflow Architecture

### Trigger Nodes
- **Webhook**: `/analyze SYMBOL` commands
- **Schedule**: Premarket analysis at 9:25 AM EST
- **Manual**: Button triggers for testing

### Processing Nodes
- **HTTP Request**: Fetch market data from APIs
- **Code Transform**: Convert API data to calculator format
- **Execute Command**: Run Python calculator
- **JSON Parser**: Parse calculator output

### Output Nodes
- **File Writer**: Save analysis to dashboard/data/
- **Telegram**: Send formatted alerts
- **Error Handler**: Log failures and retry

## 📈 Performance Specifications

### Latency Requirements
- **Analysis Time**: < 5 seconds for complete 7-algorithm analysis
- **API Response**: < 2 seconds for real-time data
- **Dashboard Update**: < 1 second for UI refresh

### Accuracy Metrics
- **Backtesting**: >70% accuracy on historical data
- **Gap Fill**: 85% accuracy for large gap predictions
- **Trend Detection**: 78% accuracy for trend changes

### Scalability Limits
- **Concurrent Symbols**: 10+ simultaneous analysis
- **API Rate Limits**: Respects provider limitations
- **Memory Usage**: < 100MB per analysis

## 🛡️ Security Architecture

### API Security
- **Environment Variables**: All keys stored securely
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize all user inputs

### Data Protection
- **Local Processing**: No sensitive data transmitted
- **Temporary Storage**: Analysis results cleaned after use
- **Access Control**: No authentication required for local use

## 🔧 Technology Stack

### Core Technologies
- **Python 3.8+**: Core calculation engine
- **N8N**: Workflow automation platform
- **Chart.js**: Real-time dashboard charts
- **GitHub Actions**: CI/CD pipeline

### External APIs
- **Polygon.io**: Primary market data source
- **Alpaca Markets**: Trading execution and portfolios
- **Yahoo Finance**: Backup free data source
- **Telegram Bot API**: Real-time notifications

### Development Tools
- **pytest**: Testing framework
- **flake8**: Code linting
- **codecov**: Coverage reporting
- **GitHub**: Version control and collaboration

## 🚀 Deployment Options

### Local Development
```bash
# Quick start for development
git clone https://github.com/RamsesAguirre777/trading-analysis-mvp.git
pip install -r requirements.txt
python src/trading_calculator.py --input data/nvda_test_data.json --pretty
```

### Production Deployment
```bash
# Docker deployment (future)
docker build -t trading-analysis-mvp .
docker run -d -p 8080:8080 trading-analysis-mvp

# Cloud deployment options
# - AWS Lambda for calculator
# - Heroku for dashboard
# - n8n Cloud for workflows
```

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 1GB for installation + data
- **Network**: Internet connection for API access

### Recommended Setup
- **Python**: 3.10+ for best performance
- **RAM**: 8GB for multiple concurrent analyses
- **Storage**: SSD for faster I/O operations
- **Network**: Stable broadband for real-time data

## 🔄 Future Architecture Plans

### Phase 4: Advanced Features
- **Machine Learning**: Prediction model integration
- **Database**: PostgreSQL for historical data
- **WebSocket**: Real-time price streaming
- **Authentication**: User accounts and portfolios

### Phase 5: Enterprise Scale
- **Microservices**: Split calculator into services
- **Load Balancing**: Handle high-volume requests
- **Monitoring**: Comprehensive system monitoring
- **API Gateway**: RESTful API for external access

---

**For detailed implementation guides, see:**
- [SETUP.md](docs/SETUP.md) - Installation and configuration
- [API.md](docs/API.md) - API documentation  
- [ALGORITHMS.md](docs/ALGORITHMS.md) - Algorithm deep dive