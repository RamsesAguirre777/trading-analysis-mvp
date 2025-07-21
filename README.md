# Trading Analysis MVP - Core Calculator

## 🎯 OVERVIEW
Core trading calculator implementing 7 algorithms for comprehensive market analysis. This is the **brain** of the trading system that analyzes stocks and crypto using multiple technical indicators.

## 🧮 ALGORITHMS IMPLEMENTED

### 1. Gap Analysis
- Calculates gap size and direction between previous close and current price
- Classifies gaps: small (<1%), medium (1-3%), large (>3%)
- Provides gap fill probability

### 2. Bollinger Bands Imbalance Analysis
- Compares premarket vs market close BBT/BBB levels
- Calculates imbalance ratios and direction
- Determines strength of imbalance

### 3. EMA Trend Analysis
- Analyzes EMA20, EMA50, EMA200 relationships
- Determines short, medium, and long-term trends
- Calculates overall trend strength

### 4. Multi-timeframe Alerts
- Compares current price vs BBT levels across timeframes
- Generates overbought/oversold alerts
- Provides correction level expectations

### 5. Directional Targets
- Identifies day high/low as directional targets
- Predicts which target will be hit first
- Uses momentum and distance analysis

### 6. Break Point Analysis
- Analyzes user-provided manual break points
- Calculates distances to resistance/support levels
- Provides breakout probability

### 7. Final Decision Engine
- Combines all algorithms for final trading signals
- Generates primary direction (LONG/SHORT)
- Provides entry levels, stop loss, and take profit
- Calculates confidence and risk/reward ratio

## 🚀 USAGE

### Basic CLI Usage
```bash
python src/trading_calculator.py --input data/nvda_test_data.json --pretty
```

### With Output File
```bash
python src/trading_calculator.py --input data/nvda_test_data.json --output results/analysis.json --pretty
```

## 📋 INPUT FORMAT
```json
{
  "symbol": "NVDA",
  "previous_day": {
    "high": 165.49,
    "low": 162.02,
    "close": 163.87,
    "change": 3.47
  },
  "current_day": {
    "high": 172.81,
    "low": 169.91,
    "current_price": 171.89,
    "change": 2.90
  },
  "manual_break_points": {
    "break_point": 171.67,
    "max_pos_exp": 174.04,
    "int_pos_exp": 172.85,
    "int_neg_exp": 170.48,
    "max_neg_exp": 169.29
  },
  "bollinger_bands": {
    "premarket_bbt_1h": 174.54,
    "premarket_bbb_1h": 160.82,
    "market_close_bbt_1h": 166.74,
    "market_close_bbb_1h": 161.84
  },
  "emas_1h": {
    "ema20": 167.68,
    "ema50": 164.25,
    "ema200": 152.47
  }
}
```

## 📤 OUTPUT FORMAT
```json
{
  "analysis_timestamp": "2025-07-21T01:20:26.256811Z",
  "symbol": "NVDA",
  "gap_analysis": {
    "gap_size": 8.02,
    "gap_direction": "up",
    "gap_percentage": 4.9,
    "fill_probability": 0.85,
    "classification": "large"
  },
  "trading_signals": {
    "primary_direction": "SHORT",
    "confidence": 0.57,
    "entry_levels": [172.06, 172.41],
    "stop_loss": 174.47,
    "take_profit": [169.91, 166.51],
    "risk_reward": 0.8
  }
}
```

## 🔧 INSTALLATION
```bash
cd trading-analysis-mvp
pip install -r requirements.txt
```

## 🧪 TESTING
```bash
# Test with included NVDA data
python src/trading_calculator.py --input data/nvda_test_data.json --pretty
```

## 📊 EXAMPLE RESULTS

With the provided NVDA test data, the system correctly identifies:
- **Large gap up** (4.9%) with high fill probability (85%)
- **Bullish trend** across all timeframes
- **High overbought** conditions suggesting correction
- **SHORT signal** despite bullish trend due to overbought conditions and large gap
- **Risk/reward ratio** of 0.8:1

## ⚡ NEXT STEPS

1. **Phase 2**: n8n workflow integration
2. **Phase 3**: Dashboard UI implementation
3. **Phase 4**: Alpaca API integration
4. **Phase 5**: Real-time alerts and automation

## 🎯 SUCCESS METRICS
- ✅ **Analysis Speed**: < 5 seconds for complete analysis
- ✅ **CLI Interface**: Fully functional with argparse
- ✅ **Data Format**: Exact JSON input/output as specified
- ✅ **All 7 Algorithms**: Implemented and tested
- ✅ **Test Data**: NVDA example working perfectly

---

**Ready for Phase 2: n8n Integration** 🚀