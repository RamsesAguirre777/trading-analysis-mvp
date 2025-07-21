#!/usr/bin/env python3
"""
Trading Analysis MVP - Core Calculator
Sistema de análisis de trading algorítmico con 7 componentes de análisis

Author: Trading MVP Team  
Version: 1.0.0
"""

import json
import argparse
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import math


class TradingCalculator:
    """
    Calculadora principal de análisis de trading que implementa 7 algoritmos:
    1. Gap Analysis
    2. Imbalance Analysis (BBT/BBB) 
    3. Trend Analysis (EMAs)
    4. Multi-timeframe Alerts
    5. Directional Targets
    6. Break Point Analysis
    7. Final Decision Engine
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.supported_markets = ["stocks", "crypto"]
    
    def analyze_symbol(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Función principal que analiza un símbolo usando todos los algoritmos
        
        Args:
            data: Diccionario con todos los datos de mercado necesarios
            
        Returns:
            Diccionario con análisis completo y señales de trading
        """
        try:
            # Validar datos de entrada
            self._validate_input_data(data)
            
            # Ejecutar todos los algoritmos de análisis
            gap_analysis = self._calculate_gap_analysis(data)
            imbalance_analysis = self._calculate_imbalance_analysis(data)
            trend_analysis = self._calculate_trend_analysis(data)
            alerts = self._calculate_multiframe_alerts(data)
            directional_targets = self._calculate_directional_targets(data)
            break_point_analysis = self._calculate_break_point_analysis(data)
            
            # Motor de decisión final
            trading_signals = self._generate_trading_signals(
                gap_analysis, imbalance_analysis, trend_analysis, 
                alerts, directional_targets, break_point_analysis, data
            )
            
            # Construir resultado final
            result = {
                "analysis_timestamp": datetime.now().isoformat(),
                "symbol": data.get("symbol", "UNKNOWN"),
                "gap_analysis": gap_analysis,
                "imbalance_analysis": imbalance_analysis,
                "trend_analysis": trend_analysis,
                "alerts": alerts,
                "directional_targets": directional_targets,
                "break_point_analysis": break_point_analysis,
                "trading_signals": trading_signals,
                "system_info": {
                    "version": self.version,
                    "components_executed": 7,
                    "analysis_complete": True
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "error": True,
                "error_message": str(e),
                "analysis_timestamp": datetime.now().isoformat(),
                "symbol": data.get("symbol", "UNKNOWN")
            }
    
    def _validate_input_data(self, data: Dict[str, Any]) -> None:
        """Valida que los datos de entrada tengan la estructura correcta"""
        required_fields = ["symbol", "previous_day", "current_day"]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido faltante: {field}")
        
        # Validar previous_day
        prev_day = data["previous_day"]
        required_prev = ["high", "low", "close", "change"]
        for field in required_prev:
            if field not in prev_day:
                raise ValueError(f"Campo faltante en previous_day: {field}")
        
        # Validar current_day
        curr_day = data["current_day"]
        required_curr = ["high", "low", "current_price", "change"]
        for field in required_curr:
            if field not in curr_day:
                raise ValueError(f"Campo faltante en current_day: {field}")
    
    def _calculate_gap_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Algoritmo 1: Análisis de Gap
        Calcula el gap entre cierre anterior y apertura actual
        """
        previous_close = data["previous_day"]["close"]
        current_price = data["current_day"]["current_price"]
        
        # Calcular gap
        gap_size = current_price - previous_close
        gap_percentage = (gap_size / previous_close) * 100
        gap_direction = "up" if gap_size > 0 else "down" if gap_size < 0 else "flat"
        
        # Clasificar gap por tamaño
        abs_gap_percent = abs(gap_percentage)
        if abs_gap_percent < 1.0:
            classification = "small"
            fill_probability = 0.3
        elif abs_gap_percent < 3.0:
            classification = "medium"
            fill_probability = 0.6
        else:
            classification = "large"
            fill_probability = 0.85
        
        return {
            "gap_size": round(gap_size, 2),
            "gap_direction": gap_direction,
            "gap_percentage": round(gap_percentage, 2),
            "fill_probability": fill_probability,
            "classification": classification,
            "previous_close": previous_close,
            "current_opening": current_price
        }
    
    def _calculate_imbalance_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Algoritmo 2: Análisis de Imbalance BBT/BBB
        Compara niveles de Bollinger Bands entre sesiones
        """
        bb_data = data.get("bollinger_bands", {})
        
        # Obtener niveles BBT/BBB
        premarket_bbt = bb_data.get("premarket_bbt_1h", 0)
        premarket_bbb = bb_data.get("premarket_bbb_1h", 0)
        market_close_bbt = bb_data.get("market_close_bbt_1h", 0)
        market_close_bbb = bb_data.get("market_close_bbb_1h", 0)
        
        # Calcular ratios (evitar división por cero)
        bbt_ratio = premarket_bbt / market_close_bbt if market_close_bbt != 0 else 1.0
        bbb_ratio = premarket_bbb / market_close_bbb if market_close_bbb != 0 else 1.0
        
        # Determinar dirección del imbalance
        if bbt_ratio > 1.05 and bbb_ratio < 0.95:
            imbalance_direction = "strong_bullish"
            strength = "high"
        elif bbt_ratio > 1.02 and bbb_ratio < 0.98:
            imbalance_direction = "bullish"
            strength = "moderate"
        elif bbt_ratio < 0.95 and bbb_ratio > 1.05:
            imbalance_direction = "strong_bearish"
            strength = "high"
        elif bbt_ratio < 0.98 and bbb_ratio > 1.02:
            imbalance_direction = "bearish"
            strength = "moderate"
        else:
            imbalance_direction = "neutral"
            strength = "low"
        
        return {
            "bbt_ratio": round(bbt_ratio, 3),
            "bbb_ratio": round(bbb_ratio, 3),
            "imbalance_direction": imbalance_direction,
            "strength": strength,
            "premarket_levels": {
                "bbt": premarket_bbt,
                "bbb": premarket_bbb
            },
            "market_close_levels": {
                "bbt": market_close_bbt,
                "bbb": market_close_bbb
            }
        }
    
    def _calculate_trend_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Algoritmo 3: Análisis de Tendencia con EMAs
        Determina tendencia usando EMA20, EMA50, EMA200
        """
        emas = data.get("emas_1h", {})
        current_price = data["current_day"]["current_price"]
        
        ema20 = emas.get("ema20", 0)
        ema50 = emas.get("ema50", 0)
        ema200 = emas.get("ema200", 0)
        
        # Determinar tendencias
        short_term = "bullish" if current_price > ema20 else "bearish"
        medium_term = "bullish" if ema20 > ema50 else "bearish"
        long_term = "bullish" if ema50 > ema200 else "bearish"
        
        # Calcular fuerza de tendencia
        bullish_signals = sum([
            current_price > ema20,
            ema20 > ema50,
            ema50 > ema200,
            current_price > ema50,
            current_price > ema200
        ])
        
        trend_strength = bullish_signals / 5.0
        
        # Determinar tendencia general
        if bullish_signals >= 4:
            overall_trend = "strong_bullish"
        elif bullish_signals >= 3:
            overall_trend = "bullish"
        elif bullish_signals >= 2:
            overall_trend = "neutral"
        elif bullish_signals >= 1:
            overall_trend = "bearish"
        else:
            overall_trend = "strong_bearish"
        
        return {
            "short_term": short_term,
            "medium_term": medium_term,
            "long_term": long_term,
            "overall_trend": overall_trend,
            "trend_strength": round(trend_strength, 2),
            "current_vs_emas": {
                "vs_ema20": round((current_price - ema20) / ema20 * 100, 2),
                "vs_ema50": round((current_price - ema50) / ema50 * 100, 2),
                "vs_ema200": round((current_price - ema200) / ema200 * 100, 2)
            }
        }
    
    def _calculate_multiframe_alerts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Algoritmo 4: Alertas Multi-timeframe
        Compara precio actual vs niveles BBT en diferentes timeframes
        """
        current_price = data["current_day"]["current_price"]
        bb_data = data.get("bollinger_bands", {})
        
        # Niveles BBT para diferentes timeframes (simulados)
        bbt_1h = bb_data.get("premarket_bbt_1h", current_price * 1.02)
        bbt_30m = bbt_1h * 0.98  # Aproximación
        bbt_5m = bbt_1h * 0.96   # Aproximación  
        bbt_1m = bbt_1h * 0.94   # Aproximación
        
        # Calcular alertas por timeframe
        alerts = {
            "overbought_1m": current_price > bbt_1m,
            "overbought_5m": current_price > bbt_5m,
            "overbought_30m": current_price > bbt_30m,
            "overbought_1h": current_price > bbt_1h
        }
        
        # Determinar nivel de corrección esperado
        if alerts["overbought_1h"]:
            correction_level = "high"
            correction_message = "High overbought level, expect medium correction"
        elif alerts["overbought_30m"]:
            correction_level = "medium"
            correction_message = "Medium overbought level, expect price correction"
        elif alerts["overbought_5m"]:
            correction_level = "low"
            correction_message = "Overbought on 5-minute candles, expect low correction"
        elif alerts["overbought_1m"]:
            correction_level = "minimal"
            correction_message = "Slightly overbought on 1-minute candles"
        else:
            correction_level = "none"
            correction_message = "No overbought conditions detected"
        
        return {
            **alerts,
            "correction_level": correction_level,
            "correction_message": correction_message,
            "timeframe_levels": {
                "bbt_1h": bbt_1h,
                "bbt_30m": bbt_30m,
                "bbt_5m": bbt_5m,
                "bbt_1m": bbt_1m
            }
        }
    
    def _calculate_directional_targets(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Algoritmo 5: Objetivos Direccionales
        Day High = objetivo alcista, Day Low = objetivo bajista
        """
        current_price = data["current_day"]["current_price"]
        day_high = data["current_day"]["high"]
        day_low = data["current_day"]["low"]
        
        # Calcular distancias
        distance_to_high = day_high - current_price
        distance_to_low = current_price - day_low
        
        # Predecir qué nivel se tocará primero
        if distance_to_high < distance_to_low:
            first_target_prediction = "bullish"
            target_distance = distance_to_high
        else:
            first_target_prediction = "bearish"
            target_distance = distance_to_low
        
        # Calcular probabilidades
        total_range = day_high - day_low
        position_in_range = (current_price - day_low) / total_range if total_range > 0 else 0.5
        
        bullish_probability = 1 - position_in_range  # Más cerca del low = más probable subir
        bearish_probability = position_in_range      # Más cerca del high = más probable bajar
        
        return {
            "bullish_target": day_high,
            "bearish_target": day_low,
            "first_target_prediction": first_target_prediction,
            "target_distance": round(target_distance, 2),
            "position_in_range": round(position_in_range, 2),
            "probabilities": {
                "bullish": round(bullish_probability, 2),
                "bearish": round(bearish_probability, 2)
            },
            "range_analysis": {
                "total_range": round(total_range, 2),
                "distance_to_high": round(distance_to_high, 2),
                "distance_to_low": round(distance_to_low, 2)
            }
        }
    
    def _calculate_break_point_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Algoritmo 6: Análisis de Break Points
        Analiza niveles manuales como resistencias/soportes
        """
        manual_levels = data.get("manual_break_points", {})
        current_price = data["current_day"]["current_price"]
        
        analysis = {
            "levels_provided": False,
            "nearest_level": None,
            "level_type": None,
            "distance_to_nearest": 0,
            "levels_analysis": {}
        }
        
        if not manual_levels:
            return analysis
        
        analysis["levels_provided"] = True
        
        # Analizar cada nivel manual
        levels = {}
        min_distance = float('inf')
        nearest_level = None
        nearest_type = None
        
        for level_name, level_value in manual_levels.items():
            if level_value is not None and isinstance(level_value, (int, float)):
                distance = abs(current_price - level_value)
                direction = "above" if current_price > level_value else "below"
                
                levels[level_name] = {
                    "value": level_value,
                    "distance": round(distance, 2),
                    "direction": direction,
                    "hit_probability": max(0, 1 - (distance / current_price))
                }
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_level = level_value
                    nearest_type = level_name
        
        analysis.update({
            "nearest_level": nearest_level,
            "level_type": nearest_type,
            "distance_to_nearest": round(min_distance, 2),
            "levels_analysis": levels
        })
        
        return analysis
    
    def _generate_trading_signals(self, gap_analysis: Dict, imbalance_analysis: Dict,
                                trend_analysis: Dict, alerts: Dict, directional_targets: Dict,
                                break_point_analysis: Dict, data: Dict) -> Dict[str, Any]:
        """
        Algoritmo 7: Motor de Decisión Final
        Combina todos los análisis para generar señales de trading
        """
        current_price = data["current_day"]["current_price"]
        
        # Puntajes de cada algoritmo (-1 a 1, donde 1 = muy alcista, -1 = muy bajista)
        scores = {}
        
        # 1. Gap Analysis Score
        if gap_analysis["classification"] == "large":
            # Gap grande tiende a cerrarse
            scores["gap"] = -0.8 if gap_analysis["gap_direction"] == "up" else 0.8
        else:
            scores["gap"] = 0.3 if gap_analysis["gap_direction"] == "up" else -0.3
        
        # 2. Imbalance Score  
        imb_dir = imbalance_analysis["imbalance_direction"]
        if "strong_bullish" in imb_dir:
            scores["imbalance"] = 0.8
        elif "bullish" in imb_dir:
            scores["imbalance"] = 0.5
        elif "strong_bearish" in imb_dir:
            scores["imbalance"] = -0.8
        elif "bearish" in imb_dir:
            scores["imbalance"] = -0.5
        else:
            scores["imbalance"] = 0
        
        # 3. Trend Score
        trend_strength = trend_analysis["trend_strength"]
        if trend_analysis["overall_trend"] in ["strong_bullish", "bullish"]:
            scores["trend"] = trend_strength
        else:
            scores["trend"] = trend_strength - 1.0
        
        # 4. Alerts Score (overbought = bearish signal)
        overbought_count = sum([
            alerts["overbought_1m"], alerts["overbought_5m"],
            alerts["overbought_30m"], alerts["overbought_1h"]
        ])
        scores["alerts"] = -0.2 * overbought_count  # Más overbought = más bearish
        
        # 5. Directional Targets Score
        target_pred = directional_targets["first_target_prediction"]
        target_prob = directional_targets["probabilities"]
        if target_pred == "bullish":
            scores["directional"] = target_prob["bullish"] - 0.5
        else:
            scores["directional"] = -(target_prob["bearish"] - 0.5)
        
        # Calcular score total y confianza
        total_score = sum(scores.values())
        confidence = min(abs(total_score) / 3.0, 1.0)  # Normalizar a 0-1
        
        # Determinar dirección primaria
        if total_score > 0.5:
            primary_direction = "LONG"
        elif total_score < -0.5:
            primary_direction = "SHORT"
        else:
            primary_direction = "NEUTRAL"
        
        # Calcular niveles de entrada, stop loss y take profit
        volatility = (data["current_day"]["high"] - data["current_day"]["low"]) / current_price
        
        if primary_direction == "LONG":
            entry_levels = [
                round(current_price * 0.999, 2),
                round(current_price * 0.996, 2)
            ]
            stop_loss = round(current_price * (1 - volatility * 1.5), 2)
            take_profit = [
                round(current_price * (1 + volatility * 1.0), 2),
                round(current_price * (1 + volatility * 2.0), 2)
            ]
        elif primary_direction == "SHORT":
            entry_levels = [
                round(current_price * 1.001, 2),
                round(current_price * 1.004, 2)
            ]
            stop_loss = round(current_price * (1 + volatility * 1.5), 2)
            take_profit = [
                round(current_price * (1 - volatility * 1.0), 2),
                round(current_price * (1 - volatility * 2.0), 2)
            ]
        else:
            entry_levels = [current_price]
            stop_loss = current_price
            take_profit = [current_price]
        
        # Calcular risk/reward ratio
        if primary_direction != "NEUTRAL" and len(take_profit) > 0:
            risk = abs(current_price - stop_loss)
            reward = abs(take_profit[0] - current_price)
            risk_reward = round(reward / risk, 2) if risk > 0 else 0
        else:
            risk_reward = 0
        
        return {
            "primary_direction": primary_direction,
            "confidence": round(confidence, 2),
            "total_score": round(total_score, 2),
            "component_scores": {k: round(v, 2) for k, v in scores.items()},
            "entry_levels": entry_levels,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward,
            "volatility": round(volatility * 100, 2),  # Como porcentaje
            "recommendation": self._generate_recommendation(primary_direction, confidence, total_score)
        }
    
    def _generate_recommendation(self, direction: str, confidence: float, score: float) -> str:
        """Genera recomendación textual basada en el análisis"""
        if direction == "NEUTRAL":
            return "Wait for clearer signals. Market conditions are mixed."
        
        conf_text = "High" if confidence > 0.7 else "Medium" if confidence > 0.4 else "Low"
        action = "Strong" if abs(score) > 1.5 else "Moderate" if abs(score) > 0.8 else "Weak"
        
        return f"{action} {direction} signal with {conf_text} confidence. Consider position sizing based on confidence level."


def main():
    """Función principal para ejecutar desde línea de comandos"""
    parser = argparse.ArgumentParser(description="Trading Analysis MVP - Core Calculator")
    parser.add_argument("--input", type=str, help="JSON input file or JSON string")
    parser.add_argument("--output", type=str, help="Output file (optional)")
    parser.add_argument("--example", action="store_true", help="Run with example NVDA data")
    
    args = parser.parse_args()
    
    calculator = TradingCalculator()
    
    # Datos de ejemplo NVDA
    if args.example:
        example_data = {
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
        
        result = calculator.analyze_symbol(example_data)
        
    elif args.input:
        try:
            # Intentar cargar como archivo JSON
            try:
                with open(args.input, 'r') as f:
                    input_data = json.load(f)
            except FileNotFoundError:
                # Si no es archivo, intentar parsear como JSON string
                input_data = json.loads(args.input)
            
            result = calculator.analyze_symbol(input_data)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        print("Error: Debes proporcionar --input con datos JSON o usar --example")
        parser.print_help()
        sys.exit(1)
    
    # Guardar o imprimir resultado
    result_json = json.dumps(result, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result_json)
        print(f"Análisis guardado en: {args.output}")
    else:
        print(result_json)


if __name__ == "__main__":
    main()
