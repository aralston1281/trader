"""
Technical analysis using TA-Lib and pandas-ta.
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import logging

try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False
    logging.warning("TA-Lib not installed. Some indicators will be unavailable.")

import pandas_ta as pta

logger = logging.getLogger(__name__)


class TechnicalAnalysis:
    """Technical analysis calculations."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with OHLCV data.
        
        Args:
            df: DataFrame with columns: Open, High, Low, Close, Volume
        """
        self.df = df
        self.signals = {}
    
    def calculate_rsi(self, period: int = 14) -> float:
        """Calculate RSI indicator."""
        try:
            if HAS_TALIB:
                rsi = talib.RSI(self.df['Close'].values, timeperiod=period)
            else:
                rsi = pta.rsi(self.df['Close'], length=period)
            
            current_rsi = rsi.iloc[-1] if isinstance(rsi, pd.Series) else rsi[-1]
            return float(current_rsi) if not pd.isna(current_rsi) else 50.0
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return 50.0
    
    def calculate_macd(self) -> Dict[str, float]:
        """Calculate MACD indicator."""
        try:
            if HAS_TALIB:
                macd, signal, hist = talib.MACD(
                    self.df['Close'].values,
                    fastperiod=12,
                    slowperiod=26,
                    signalperiod=9
                )
            else:
                macd_df = pta.macd(self.df['Close'])
                macd = macd_df['MACD_12_26_9'].values
                signal = macd_df['MACDs_12_26_9'].values
                hist = macd_df['MACDh_12_26_9'].values
            
            return {
                'macd': float(macd[-1]) if not pd.isna(macd[-1]) else 0.0,
                'signal': float(signal[-1]) if not pd.isna(signal[-1]) else 0.0,
                'histogram': float(hist[-1]) if not pd.isna(hist[-1]) else 0.0,
                'bullish': hist[-1] > 0 if not pd.isna(hist[-1]) else False
            }
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {'macd': 0, 'signal': 0, 'histogram': 0, 'bullish': False}
    
    def calculate_moving_averages(self) -> Dict[str, Any]:
        """Calculate key moving averages."""
        try:
            current_price = self.df['Close'].iloc[-1]
            
            sma_20 = self.df['Close'].rolling(20).mean().iloc[-1]
            sma_50 = self.df['Close'].rolling(50).mean().iloc[-1]
            sma_200 = self.df['Close'].rolling(200).mean().iloc[-1]
            
            ema_9 = self.df['Close'].ewm(span=9).mean().iloc[-1]
            ema_21 = self.df['Close'].ewm(span=21).mean().iloc[-1]
            
            return {
                'sma_20': float(sma_20),
                'sma_50': float(sma_50),
                'sma_200': float(sma_200),
                'ema_9': float(ema_9),
                'ema_21': float(ema_21),
                'above_sma_20': current_price > sma_20,
                'above_sma_50': current_price > sma_50,
                'above_sma_200': current_price > sma_200,
                'golden_cross': sma_50 > sma_200 if not pd.isna(sma_200) else False,
                'death_cross': sma_50 < sma_200 if not pd.isna(sma_200) else False
            }
        except Exception as e:
            logger.error(f"Error calculating moving averages: {e}")
            return {}
    
    def calculate_bollinger_bands(self, period: int = 20, std: int = 2) -> Dict[str, float]:
        """Calculate Bollinger Bands."""
        try:
            if HAS_TALIB:
                upper, middle, lower = talib.BBANDS(
                    self.df['Close'].values,
                    timeperiod=period,
                    nbdevup=std,
                    nbdevdn=std
                )
            else:
                bb = pta.bbands(self.df['Close'], length=period, std=std)
                upper = bb[f'BBU_{period}_{std}.0'].values
                middle = bb[f'BBM_{period}_{std}.0'].values
                lower = bb[f'BBL_{period}_{std}.0'].values
            
            current_price = self.df['Close'].iloc[-1]
            
            return {
                'upper': float(upper[-1]),
                'middle': float(middle[-1]),
                'lower': float(lower[-1]),
                'percent_b': (current_price - lower[-1]) / (upper[-1] - lower[-1]),
                'squeeze': (upper[-1] - lower[-1]) / middle[-1] < 0.1
            }
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return {}
    
    def find_support_resistance(self, window: int = 20) -> Dict[str, list]:
        """Identify support and resistance levels."""
        try:
            highs = self.df['High'].rolling(window).max()
            lows = self.df['Low'].rolling(window).min()
            
            # Find pivot points
            resistance_levels = highs.drop_duplicates().sort_values(ascending=False).head(3).tolist()
            support_levels = lows.drop_duplicates().sort_values().head(3).tolist()
            
            current_price = self.df['Close'].iloc[-1]
            
            return {
                'resistance_levels': resistance_levels,
                'support_levels': support_levels,
                'nearest_resistance': min([r for r in resistance_levels if r > current_price], default=None),
                'nearest_support': max([s for s in support_levels if s < current_price], default=None)
            }
        except Exception as e:
            logger.error(f"Error finding support/resistance: {e}")
            return {}
    
    def calculate_volume_analysis(self) -> Dict[str, Any]:
        """Analyze volume patterns."""
        try:
            avg_volume_20 = self.df['Volume'].rolling(20).mean().iloc[-1]
            current_volume = self.df['Volume'].iloc[-1]
            
            # Volume trend
            volume_trend = self.df['Volume'].rolling(5).mean().iloc[-1] / avg_volume_20
            
            # On-Balance Volume
            obv = (np.sign(self.df['Close'].diff()) * self.df['Volume']).fillna(0).cumsum()
            obv_trend = obv.iloc[-5:].is_monotonic_increasing
            
            return {
                'avg_volume_20d': float(avg_volume_20),
                'current_volume': float(current_volume),
                'volume_ratio': float(current_volume / avg_volume_20),
                'high_volume': current_volume > avg_volume_20 * 1.5,
                'volume_trend_up': volume_trend > 1.2,
                'obv_bullish': obv_trend
            }
        except Exception as e:
            logger.error(f"Error analyzing volume: {e}")
            return {}
    
    def get_trend_strength(self) -> Dict[str, Any]:
        """Calculate overall trend strength."""
        try:
            # ADX (Average Directional Index)
            if HAS_TALIB:
                adx = talib.ADX(
                    self.df['High'].values,
                    self.df['Low'].values,
                    self.df['Close'].values,
                    timeperiod=14
                )
                current_adx = adx[-1]
            else:
                adx_df = pta.adx(self.df['High'], self.df['Low'], self.df['Close'])
                current_adx = adx_df['ADX_14'].iloc[-1] if 'ADX_14' in adx_df else 25.0
            
            # Determine trend strength
            if current_adx > 50:
                strength = "Very Strong"
            elif current_adx > 25:
                strength = "Strong"
            elif current_adx > 20:
                strength = "Moderate"
            else:
                strength = "Weak"
            
            return {
                'adx': float(current_adx),
                'strength': strength,
                'trending': current_adx > 25
            }
        except Exception as e:
            logger.error(f"Error calculating trend strength: {e}")
            return {'adx': 25.0, 'strength': 'Moderate', 'trending': False}
    
    def generate_technical_summary(self) -> Dict[str, Any]:
        """Generate comprehensive technical analysis summary."""
        try:
            rsi = self.calculate_rsi()
            macd = self.calculate_macd()
            mas = self.calculate_moving_averages()
            bb = self.calculate_bollinger_bands()
            sr = self.find_support_resistance()
            vol = self.calculate_volume_analysis()
            trend = self.get_trend_strength()
            
            # Overall bias
            bullish_signals = 0
            bearish_signals = 0
            
            # RSI
            if rsi < 30:
                bullish_signals += 2
            elif rsi > 70:
                bearish_signals += 2
            elif 40 < rsi < 60:
                pass  # neutral
            
            # MACD
            if macd['bullish']:
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            # Moving averages
            if mas.get('above_sma_50'):
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            if mas.get('golden_cross'):
                bullish_signals += 2
            elif mas.get('death_cross'):
                bearish_signals += 2
            
            # Determine overall bias
            total_signals = bullish_signals + bearish_signals
            if total_signals > 0:
                bias_score = (bullish_signals - bearish_signals) / total_signals * 10
            else:
                bias_score = 0
            
            return {
                'rsi': rsi,
                'macd': macd,
                'moving_averages': mas,
                'bollinger_bands': bb,
                'support_resistance': sr,
                'volume': vol,
                'trend': trend,
                'bias_score': bias_score,  # -10 (bearish) to +10 (bullish)
                'bullish_signals': bullish_signals,
                'bearish_signals': bearish_signals
            }
        except Exception as e:
            logger.error(f"Error generating technical summary: {e}")
            return {'bias_score': 0}


def get_technical_analysis(ticker: str, df: pd.DataFrame = None) -> Optional[Dict[str, Any]]:
    """
    Get technical analysis for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        df: Optional pre-loaded price data
        
    Returns:
        Dictionary with technical analysis results
    """
    try:
        if df is None:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            df = stock.history(period="6mo")
        
        if df.empty or len(df) < 50:
            logger.warning(f"Insufficient data for technical analysis: {ticker}")
            return None
        
        ta = TechnicalAnalysis(df)
        summary = ta.generate_technical_summary()
        summary['ticker'] = ticker
        
        return summary
        
    except Exception as e:
        logger.error(f"Error in technical analysis for {ticker}: {e}")
        return None

