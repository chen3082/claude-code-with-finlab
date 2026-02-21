"""
headless_backtest.py — 無頭回測執行器

用法:
    python tools/headless_backtest.py strategies/your_strategy.py

輸出:
    回測 KPI: CAGR, MDD, Sharpe, 勝率 等核心指標
"""

import os
import sys
import traceback
import importlib.util
from dotenv import load_dotenv

load_dotenv()

import finlab
from finlab import data
from finlab.backtest import sim

def run_backtest(strategy_path: str):
    print(f"\n{'='*60}")
    print(f"  Project Pickaxe — Headless Backtest Runner")
    print(f"  策略檔案: {strategy_path}")
    print(f"{'='*60}\n")

    # --- 登入 ---
    token = os.getenv("FINLAB_API_TOKEN")
    if not token:
        print("[ERROR] 找不到 FINLAB_API_TOKEN，請確認 .env 設定。")
        sys.exit(1)
    finlab.login(token)

    # --- 動態載入策略模組 ---
    spec = importlib.util.spec_from_file_location("strategy", strategy_path)
    if spec is None:
        print(f"[ERROR] 無法載入策略檔案: {strategy_path}")
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"[ERROR] 策略執行失敗:\n")
        traceback.print_exc()
        sys.exit(1)

    # --- 取得 position ---
    if not hasattr(module, "position"):
        print("[ERROR] 策略檔案必須產生一個名為 `position` 的 DataFrame。")
        sys.exit(1)

    position = module.position

    # --- 執行回測 ---
    print("[INFO] 開始回測...\n")
    try:
        report = sim(
            position,
            resample=getattr(module, "RESAMPLE", "W"),
            fee_ratio=getattr(module, "FEE_RATIO", 1.425 / 1000),
            tax_ratio=getattr(module, "TAX_RATIO", 3 / 1000),
        )
    except Exception as e:
        print(f"[ERROR] 回測引擎發生錯誤:\n")
        traceback.print_exc()
        sys.exit(1)

    # --- 印出 KPI ---
    print("\n" + "="*60)
    print("  回測結果 KPI")
    print("="*60)

    stats = report.get_stats()
    kpi_keys = [
        "total_return",
        "cagr",
        "mdd",
        "sharpe",
        "win_rate",
        "trade_count",
    ]
    labels = {
        "total_return": "總報酬率",
        "cagr":         "年化報酬率 (CAGR)",
        "mdd":          "最大回撤 (MDD)",
        "sharpe":       "夏普比率",
        "win_rate":     "勝率",
        "trade_count":  "總交易次數",
    }

    for key in kpi_keys:
        if key in stats:
            val = stats[key]
            if isinstance(val, float):
                print(f"  {labels.get(key, key):<25} {val:.2%}" if "rate" in key or key in ("cagr","mdd","total_return") else f"  {labels.get(key, key):<25} {val:.4f}")
            else:
                print(f"  {labels.get(key, key):<25} {val}")

    print("="*60)

    # --- MDD 警告 ---
    mdd = stats.get("mdd", 0)
    if abs(mdd) > 0.3:
        print(f"\n[WARNING] MDD 超過 30% ({mdd:.1%})，建議考慮以下濾網：")
        print("  - 加入月線 / 季線多頭排列條件")
        print("  - 加入三大法人籌碼過濾（外資連續買超 N 日）")
        print("  - 加入成交量放大確認（量能 > 5日均量）")

    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python tools/headless_backtest.py strategies/<檔案>.py")
        sys.exit(1)

    strategy_file = sys.argv[1]

    if not os.path.exists(strategy_file):
        print(f"[ERROR] 找不到策略檔案: {strategy_file}")
        sys.exit(1)

    run_backtest(strategy_file)
