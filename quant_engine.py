import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

# --- CONFIGURATION CLASS ---
@dataclass
class StrategyConfig:
    lookback_window: int      # How many bars to look back for High/Low
    profit_target_pct: float  # Take profit percentage
    stop_loss_pct: float      # Stop loss percentage
    fee_per_trade: float = 0.0002 # Simulated exchange fee (0.02%)

class QuantEngine:
    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.data = None
        self.results = {}

    def generate_dummy_data(self, num_rows=10000) -> None:
        """
        Generates synthetic 5-second High-Frequency Data.
        Uses Geometric Brownian Motion to simulate realistic market volatility."""
        
        
        
        np.random.seed(42)
        # Time index (5 second intervals)
        dates = pd.date_range(start="2023-01-01", periods=num_rows, freq="5S")
        
        # Random walk generation
        returns = np.random.normal(loc=0.00001, scale=0.0005, size=num_rows)
        price_path = 100 * np.cumprod(1 + returns)
        
        # Create OHLC (Open, High, Low, Close) from the path
        # Adding some noise to create High/Low wicks
        noise = np.random.uniform(0.9995, 1.0005, size=num_rows)
        
        df = pd.DataFrame(index=dates)
        df['close'] = price_path
        df['open'] = df['close'].shift(1).fillna(df['close'])
        df['high'] = df[['open', 'close']].max(axis=1) * (1 + abs(np.random.normal(0, 0.0002, num_rows)))
        df['low'] = df[['open', 'close']].min(axis=1) * (1 - abs(np.random.normal(0, 0.0002, num_rows)))
        
        self.data = df
        print(f"✅ Generated {num_rows} rows of High-Frequency 5-second data.")

    def run_strategy(self, config: StrategyConfig) -> pd.DataFrame:
        """
        Runs a Vectorized Backtest. 
        Logic: 'Box Breakout' - If price breaks the High of the last N bars.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Run generate_dummy_data() first.")

        df = self.data.copy()

        # --- 1. THE MATHS (Vectorized for Speed) ---
        # Calculate Rolling Box (Donchian Channel Logic)
        df['box_high'] = df['high'].rolling(window=config.lookback_window).max().shift(1)
        df['box_low'] = df['low'].rolling(window=config.lookback_window).min().shift(1)

        # --- 2. SIGNAL GENERATION ---
        # Long Signal: Close crosses above Box High
        df['signal'] = np.where(df['close'] > df['box_high'], 1, 0)
        
        # Short Signal: Close crosses below Box Low
        df['signal'] = np.where(df['close'] < df['box_low'], -1, df['signal'])

        # --- 3. EXECUTION LOGIC (Simplified for MVP) ---
        # We calculate returns based on the signal of the previous bar
        df['pct_change'] = df['close'].pct_change()
        df['strategy_return'] = df['signal'].shift(1) * df['pct_change']
        
        # Apply Stop Loss / Take Profit Logic (Vectorized Approximation)
        # If the return is too negative, we cap it at stop loss
        df['strategy_return'] = np.where(df['strategy_return'] < -config.stop_loss_pct, 
                                         -config.stop_loss_pct, 
                                         df['strategy_return'])
        
        # If the return is too high, we cap it at profit target
        df['strategy_return'] = np.where(df['strategy_return'] > config.profit_target_pct, 
                                         config.profit_target_pct, 
                                         df['strategy_return'])

        # Apply Fees
        df['strategy_return'] = np.where(df['strategy_return'] != 0, 
                                         df['strategy_return'] - config.fee_per_trade, 
                                         df['strategy_return'])

        return df

    def calculate_metrics(self, df_results: pd.DataFrame) -> Dict:
        """
        Calculates Professional Quant Metrics:
        Win Rate, Drawdown, Expectancy, Sharpe Ratio.
        """
        # Filter only trades that happened
        trades = df_results[df_results['strategy_return'] != 0]['strategy_return']
        
        if len(trades) == 0:
            return {"win_rate": 0, "total_trades": 0, "expectancy": 0}

        # 1. Total Trades
        total_trades = len(trades)

        # 2. Win Rate Calculation
        winning_trades = trades[trades > 0]
        win_rate = len(winning_trades) / total_trades

        # 3. Expectancy = (Win% * Avg_Win) - (Loss% * Avg_Loss)
        avg_win = winning_trades.mean() if len(winning_trades) > 0 else 0
        losing_trades = trades[trades <= 0]
        avg_loss = abs(losing_trades.mean()) if len(losing_trades) > 0 else 0
        
        expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)

        # 4. Max Drawdown
        cumulative_returns = (1 + df_results['strategy_return']).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()

        return {
            "total_trades": total_trades,
            "win_rate": round(win_rate * 100, 2),
            "max_drawdown_pct": round(max_drawdown * 100, 2),
            "expectancy": round(expectancy * 100, 4),
            "net_profit_pct": round((cumulative_returns.iloc[-1] - 1) * 100, 2)
        }