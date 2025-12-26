import pandas as pd
import itertools
import time
from quant_engine import QuantEngine, StrategyConfig

def main():
    print("🚀 Initializing Quant Backtesting System...")
    print("---------------------------------------------")

    # 1. Initialize Engine & Data
    engine = QuantEngine()
    engine.generate_dummy_data(num_rows=20000) # Simulating ~27 hours of 5-sec data

    # 2. Define Parameter Grid (The "Variables" we want to test)
    # We will test different window sizes and Stop Losses to see what works best
    lookback_windows = [10, 20, 50, 100]
    stop_losses = [0.001, 0.002, 0.005] # 0.1%, 0.2%, 0.5%
    take_profits = [0.002, 0.005, 0.01]

    # Create all combinations of parameters
    combinations = list(itertools.product(lookback_windows, stop_losses, take_profits))
    
    print(f"⚙️  Running Optimization on {len(combinations)} unique configurations...")
    print("---------------------------------------------")

    results_log = []

    start_time = time.time()

    # 3. Loop through combinations (The "Simulations")
    for window, sl, tp in combinations:
        
        config = StrategyConfig(
            lookback_window=window,
            stop_loss_pct=sl,
            profit_target_pct=tp
        )

        # Run the backtest
        df_backtest = engine.run_strategy(config)
        
        # Get the math stats
        metrics = engine.calculate_metrics(df_backtest)

        # Store results
        results_log.append({
            "Window": window,
            "StopLoss": sl,
            "TakeProfit": tp,
            "WinRate": metrics['win_rate'],
            "Trades": metrics['total_trades'],
            "Drawdown": metrics['max_drawdown_pct'],
            "Expectancy": metrics['expectancy']
        })

    # 4. Process Results
    results_df = pd.DataFrame(results_log)
    
    # Sort by Win Rate (Highest first) as requested by client
    best_configs = results_df.sort_values(by="WinRate", ascending=False)

    end_time = time.time()

    print("\n✅ OPTIMIZATION COMPLETE")
    print(f"⏱️  Time taken: {round(end_time - start_time, 2)} seconds")
    print("---------------------------------------------")
    
    print("\n🏆 TOP 5 CONFIGURATIONS (Sorted by Win Rate):")
    print(best_configs.head(5).to_string(index=False))

    # Check if any met the 80% criteria
    high_win_rate = best_configs[best_configs['WinRate'] >= 80]
    
    if not high_win_rate.empty:
        print("\n✨ SUCCESS: Found configurations with > 80% Win Rate!")
        print(f"   --> Recommended Config: Window={high_win_rate.iloc[0]['Window']}, "
              f"SL={high_win_rate.iloc[0]['StopLoss']}, TP={high_win_rate.iloc[0]['TakeProfit']}")
    else:
        print("\n⚠️  NOTE: No config reached 80% win rate with this dummy data.")
        print("   (This is expected with random data. Real market data will show patterns.)")

if __name__ == "__main__":
    main()