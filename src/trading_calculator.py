#!/usr/bin/env python3
"""
Trading Analysis MVP - Core Calculator
Implements 7 trading algorithms for comprehensive market analysis

Author: Claude Code
Version: 1.0.0
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Any
import numpy as np


class TradingCalculator:
    """
    Core trading calculator implementing 7 algorithms:
    1. Gap Analysis
    2. Bollinger Bands Imbalance Analysis  
    3. EMA Trend Analysis
    4. Multi-timeframe Alerts
    5. Directional Targets
    6. Break Point Analysis
    7. Final Decision Engine
    """
    
    def __init__(self):
        self.analysis_result = {}
    
    def analyze_symbol(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis function combining all 7 algorithms
        
        Args:
            data: JSON input with market data
            
        Returns:
            Complete analysis with trading signals
        """
        symbol = data.get('symbol', 'UNKNOWN')
        
        # Initialize result structure
        self.analysis_result = {
            "analysis_timestamp": datetime.now().isoformat() + "Z",
            "symbol": symbol
        }
        
        # Execute all 7 algorithms
        self._gap_analysis(data)
        self._imbalance_analysis(data)
        self._trend_analysis(data)
        self._multi_timeframe_alerts(data)
        self._directional_targets(data)
        self._break_point_analysis(data)
        self._final_decision_engine(data)
        
        return self.analysis_result
    
    def _gap_analysis(self, data: Dict[str, Any]) -> None:
        """
        Algorithm 1: Gap Analysis
        Calculates gap size, direction and fill probability
        """
        previous_close = data['previous_day']['close']
        current_price = data['current_day']['current_price']
        
        gap_size = current_price - previous_close
        gap_percentage = (gap_size / previous_close) * 100
        gap_direction = "up" if gap_size > 0 else "down"
        
        # Classification based on percentage
        if abs(gap_percentage) < 1:
            classification = "small"
            fill_probability = 0.3
        elif abs(gap_percentage) < 3:
            classification = "medium"
            fill_probability = 0.6
        else:
            classification = "large"
            fill_probability = 0.85
        
        self.analysis_result["gap_analysis"] = {
            "gap_size": round(gap_size, 2),
            "gap_direction": gap_direction,
            "gap_percentage": round(gap_percentage, 1),
            "fill_probability": fill_probability,
            "classification": classification
        }
    
    def _imbalance_analysis(self, data: Dict[str, Any]) -> None:
        """
        Algorithm 2: Bollinger Bands Imbalance Analysis
        Compares premarket vs market close BBT/BBB levels
        """
        bb = data['bollinger_bands']
        
        # Calculate ratios
        bbt_ratio = bb['premarket_bbt_1h'] / bb['market_close_bbt_1h']
        bbb_ratio = bb['premarket_bbb_1h'] / bb['market_close_bbb_1h']
        
        # Determine imbalance direction
        if bbt_ratio > 1.02 and bbb_ratio > 0.98:
            imbalance_direction = "bullish"
            strength = "strong" if bbt_ratio > 1.05 else "moderate"
        elif bbt_ratio < 0.98 and bbb_ratio < 1.02:
            imbalance_direction = "bearish"
            strength = "strong" if bbt_ratio < 0.95 else "moderate"
        else:
            imbalance_direction = "neutral"
            strength = "weak"
        
        self.analysis_result["imbalance_analysis"] = {
            "bbt_ratio": round(bbt_ratio, 3),
            "bbb_ratio": round(bbb_ratio, 3),
            "imbalance_direction": imbalance_direction,
            "strength": strength
        }
    
    def _trend_analysis(self, data: Dict[str, Any]) -> None:
        """
        Algorithm 3: EMA Trend Analysis
        Analyzes EMA20, EMA50, EMA200 relationships
        """
        emas = data['emas_1h']
        current_price = data['current_day']['current_price']
        
        ema20 = emas['ema20']
        ema50 = emas['ema50']
        ema200 = emas['ema200']
        
        # Short-term trend (price vs EMA20)
        short_term = "bullish" if current_price > ema20 else "bearish"
        
        # Medium-term trend (EMA20 vs EMA50)
        medium_term = "bullish" if ema20 > ema50 else "bearish"
        
        # Long-term trend (EMA50 vs EMA200)
        long_term = "bullish" if ema50 > ema200 else "bearish"
        
        # Calculate trend strength
        bullish_signals = sum([
            current_price > ema20,
            ema20 > ema50,
            ema50 > ema200,
            current_price > ema50,
            current_price > ema200
        ])
        
        trend_strength = bullish_signals / 5.0
        
        self.analysis_result["trend_analysis"] = {
            "short_term": short_term,
            "medium_term": medium_term,
            "long_term": long_term,
            "trend_strength": round(trend_strength, 2)
        }
    
    def _multi_timeframe_alerts(self, data: Dict[str, Any]) -> None:
        """
        Algorithm 4: Multi-timeframe Alerts
        Compares current price vs BBT levels for overbought/oversold
        """
        current_price = data['current_day']['current_price']
        bb = data['bollinger_bands']
        
        # Compare with previous day BBT levels (for stocks premarket analysis)
        bbt_1h = bb['market_close_bbt_1h']
        bbb_1h = bb['market_close_bbb_1h']
        
        # Simulate different timeframe levels (would come from real BBT calculations)
        bbt_30m = bbt_1h * 0.98  # Slightly lower than 1H
        bbt_5m = bbt_1h * 0.96   # Lower than 30M
        bbt_1m = bbt_1h * 0.94   # Lowest
        
        # Check overbought conditions
        overbought_1h = current_price > bbt_1h
        overbought_30m = current_price > bbt_30m
        overbought_5m = current_price > bbt_5m
        overbought_1m = current_price > bbt_1m
        
        # Determine correction level
        if overbought_1h:
            correction_level = "high"
        elif overbought_30m:
            correction_level = "medium"
        elif overbought_5m:
            correction_level = "low"
        elif overbought_1m:
            correction_level = "slight"
        else:
            correction_level = "none"
        
        self.analysis_result["alerts"] = {
            "overbought_1m": overbought_1m,
            "overbought_5m": overbought_5m,
            "overbought_30m": overbought_30m,
            "overbought_1h": overbought_1h,
            "correction_level": correction_level
        }
    
    def _directional_targets(self, data: Dict[str, Any]) -> None:
        """
        Algorithm 5: Directional Targets
        Predicts which level (day high/low) will be hit first
        """
        current_price = data['current_day']['current_price']
        day_high = data['current_day']['high']
        day_low = data['current_day']['low']
        
        # Calculate distances
        distance_to_high = day_high - current_price
        distance_to_low = current_price - day_low
        
        # Predict first target based on momentum and distance
        gap_direction = self.analysis_result["gap_analysis"]["gap_direction"]
        trend_strength = self.analysis_result["trend_analysis"]["trend_strength"]
        
        # Logic: closer target + trend direction
        if distance_to_high < distance_to_low:
            if gap_direction == "up" and trend_strength > 0.6:
                first_target_prediction = "bullish"
            else:
                first_target_prediction = "bearish"  # Reversal likely
        else:
            if gap_direction == "down" and trend_strength < 0.4:
                first_target_prediction = "bearish"
            else:
                first_target_prediction = "bullish"  # Bounce likely
        
        self.analysis_result["directional_targets"] = {
            "bullish_target": day_high,
            "bearish_target": day_low,
            "first_target_prediction": first_target_prediction
        }
    
    def _break_point_analysis(self, data: Dict[str, Any]) -> None:
        """
        Algorithm 6: Break Point Analysis
        Analyzes manual break points and expansion levels
        """
        manual_levels = data.get('manual_break_points', {})
        current_price = data['current_day']['current_price']
        
        if not manual_levels:
            self.analysis_result["break_point_analysis"] = {
                "break_point_distance": None,
                "nearest_resistance": None,
                "nearest_support": None,
                "probability_break_up": 0.5
            }
            return
        
        break_point = manual_levels.get('break_point')
        max_pos_exp = manual_levels.get('max_pos_exp')
        int_pos_exp = manual_levels.get('int_pos_exp')
        int_neg_exp = manual_levels.get('int_neg_exp')
        max_neg_exp = manual_levels.get('max_neg_exp')
        
        # Calculate distances
        break_point_distance = current_price - break_point if break_point else None
        
        # Find nearest resistance and support
        resistances = [level for level in [break_point, int_pos_exp, max_pos_exp] if level and level > current_price]
        supports = [level for level in [break_point, int_neg_exp, max_neg_exp] if level and level < current_price]
        
        nearest_resistance = min(resistances) if resistances else None
        nearest_support = max(supports) if supports else None
        
        # Calculate break probability based on momentum
        trend_strength = self.analysis_result["trend_analysis"]["trend_strength"]
        gap_momentum = abs(self.analysis_result["gap_analysis"]["gap_percentage"]) / 10
        
        probability_break_up = min(0.9, max(0.1, trend_strength * 0.7 + gap_momentum * 0.3))
        
        self.analysis_result["break_point_analysis"] = {
            "break_point_distance": round(break_point_distance, 2) if break_point_distance else None,
            "nearest_resistance": nearest_resistance,
            "nearest_support": nearest_support,
            "probability_break_up": round(probability_break_up, 2)
        }
    
    def _final_decision_engine(self, data: Dict[str, Any]) -> None:
        """
        Algorithm 7: Final Decision Engine
        Combines all algorithms to generate trading signals
        """
        current_price = data['current_day']['current_price']
        
        # Get analysis results
        gap_analysis = self.analysis_result["gap_analysis"]
        trend_analysis = self.analysis_result["trend_analysis"]
        alerts = self.analysis_result["alerts"]
        directional_targets = self.analysis_result["directional_targets"]
        
        # Calculate overall signals
        bullish_factors = 0
        bearish_factors = 0
        
        # Gap analysis influence
        if gap_analysis["gap_direction"] == "up":
            if gap_analysis["classification"] == "large":
                bearish_factors += 2  # Large gap likely to fill
            else:
                bullish_factors += 1
        else:
            bearish_factors += 1
        
        # Trend analysis influence
        if trend_analysis["trend_strength"] > 0.6:
            bullish_factors += 2
        elif trend_analysis["trend_strength"] < 0.4:
            bearish_factors += 2
        
        # Overbought/oversold influence
        if alerts["correction_level"] in ["high", "medium"]:
            bearish_factors += 2
        elif alerts["correction_level"] == "low":
            bearish_factors += 1
        
        # Directional targets influence
        if directional_targets["first_target_prediction"] == "bullish":
            bullish_factors += 1
        else:
            bearish_factors += 1
        
        # Determine primary direction
        if bullish_factors > bearish_factors:
            primary_direction = "LONG"
            confidence = min(0.9, bullish_factors / (bullish_factors + bearish_factors))
        else:
            primary_direction = "SHORT"
            confidence = min(0.9, bearish_factors / (bullish_factors + bearish_factors))
        
        # Calculate entry levels
        if primary_direction == "LONG":
            entry_levels = [
                round(current_price * 0.999, 2),
                round(current_price * 0.997, 2)
            ]
            stop_loss = round(current_price * 0.985, 2)
            take_profit = [
                directional_targets["bullish_target"],
                round(directional_targets["bullish_target"] * 1.02, 2)
            ]
        else:
            entry_levels = [
                round(current_price * 1.001, 2),
                round(current_price * 1.003, 2)
            ]
            stop_loss = round(current_price * 1.015, 2)
            take_profit = [
                directional_targets["bearish_target"],
                round(directional_targets["bearish_target"] * 0.98, 2)
            ]
        
        # Calculate risk/reward ratio
        risk = abs(current_price - stop_loss)
        reward = abs(take_profit[0] - current_price)
        risk_reward = round(reward / risk, 1) if risk > 0 else 1.0
        
        self.analysis_result["trading_signals"] = {
            "primary_direction": primary_direction,
            "confidence": round(confidence, 2),
            "entry_levels": entry_levels,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward
        }


def main():
    """CLI interface for trading calculator"""
    parser = argparse.ArgumentParser(description='Trading Analysis MVP - Core Calculator')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file with market data')
    parser.add_argument('--output', '-o', help='Output JSON file (optional)')
    parser.add_argument('--pretty', '-p', action='store_true', help='Pretty print output')
    
    args = parser.parse_args()
    
    try:
        # Load input data
        with open(args.input, 'r') as f:
            input_data = json.load(f)
        
        # Create calculator and analyze
        calculator = TradingCalculator()
        result = calculator.analyze_symbol(input_data)
        
        # Format output
        if args.pretty:
            output = json.dumps(result, indent=2)
        else:
            output = json.dumps(result)
        
        # Save or print output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Analysis saved to {args.output}")
        else:
            print(output)
    
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in input file '{args.input}'")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())