# Claude Code × FinLab — 台股造鏟者探勘系統

> Use **Claude Code** as an AI pair-programmer to research, build, and backtest Taiwan stock quantitative strategies with the **FinLab** library.

---

## What This Is

This repo is a **Claude Code workspace template** for Taiwan stock quant development.

Instead of writing boilerplate yourself, Claude Code reads the docs, searches the database, writes strategies, runs backtests, and interprets results — all from your terminal.

```
You: "幫我寫一個月營收年增率 > 20% 且站上月線的策略"
Claude: [reads docs] → [searches DB] → [writes strategy] → [runs backtest] → [reports CAGR/MDD]
```

---

## Prerequisites

### 1. Claude Code
Install the CLI:
```bash
npm install -g @anthropic/claude-code
```
You need an [Anthropic API key](https://console.anthropic.com/).

### 2. FinLab Account + API Token
Sign up at [ai.finlab.tw](https://ai.finlab.tw) and get your API token.

> **VIP membership** is strongly recommended — free tier has limited data history and fields.

### 3. Python Environment
```bash
pip install finlab python-dotenv
```

Optional (for technical indicators):
```bash
pip install ta-lib pandas-ta
```

---

## Setup

### 1. Clone this repo
```bash
git clone https://github.com/chen3082/claude-code-with-finlab.git
cd claude-code-with-finlab
```

### 2. Create your `.env` file
```bash
cp .env.example .env
```
Edit `.env` and fill in your token:
```
FINLAB_API_TOKEN=your_token_here
```
> `.env` is git-ignored and will never be committed.

### 3. Create your `strategies/` folder
```bash
mkdir -p strategies
```
Your strategy `.py` files go here. This folder is also git-ignored — your alpha stays private.

### 4. Launch Claude Code
```bash
claude
```

---

## Folder Structure

```
claude-code-with-finlab/
├── CLAUDE.md                  # Claude's persona, rules, and workflow
├── .env                       # 🔒 Your API token (git-ignored, create manually)
│
├── docs/                      # Knowledge base — Claude reads these before writing code
│   ├── finlab_api_guide.md    # FinLab API reference (data, dataframe, backtest)
│   ├── data_catalog.md        # Taiwan stock data field dictionary
│   └── pickaxe_system.md      # (Optional) Your system design spec
│
├── tools/                     # Scripts that give Claude terminal superpowers
│   ├── search_db.py           # Search FinLab database for exact field strings
│   └── headless_backtest.py   # Run backtests and print KPIs to terminal
│
└── strategies/                # 🔒 Your strategy .py files (git-ignored, stays local)
    └── .gitkeep
```

### What Each Part Does

| File/Folder | Purpose |
|-------------|---------|
| `CLAUDE.md` | The "system prompt" for your workspace. Tells Claude what rules to follow, what tools to use, and how to develop strategies. |
| `docs/finlab_api_guide.md` | Prevents Claude from hallucinating APIs. Sourced directly from the official FinLab docs. |
| `docs/data_catalog.md` | Taiwan stock field names are exact strings. Claude checks here first. |
| `tools/search_db.py` | When a field isn't in the catalog, Claude runs this to find the correct string from the live database. |
| `tools/headless_backtest.py` | Claude runs your strategy through this and reads the CAGR/MDD output directly. |
| `strategies/` | Where Claude saves each strategy file it writes. Git-ignored so your logic stays private. |

---

## How to Use

### Ask Claude to build a strategy
```
幫我建立一個策略：月營收年增率 > 20%，且股價站上 20 日均線，每月換股
```

Claude will:
1. Check `docs/data_catalog.md` for correct field strings
2. Run `python tools/search_db.py` if needed
3. Write a strategy to `strategies/your_strategy.py`
4. Run `python tools/headless_backtest.py strategies/your_strategy.py`
5. Report CAGR, MDD, Sharpe back to you
6. Suggest filters (moving average, chip data) if MDD is too high

### Search available data fields manually
```bash
python tools/search_db.py 營收
python tools/search_db.py 外資
python tools/search_db.py ROE
```

### Run a backtest manually
```bash
python tools/headless_backtest.py strategies/my_strategy.py
```

---

## Strategy File Template

Every strategy Claude writes follows this pattern:

```python
import os
from dotenv import load_dotenv
import finlab
from finlab import data
from finlab.backtest import sim

load_dotenv()
finlab.login(os.getenv("FINLAB_API_TOKEN"))

# --- Data ---
close   = data.get('price:收盤價')
revenue = data.get('monthly_revenue:當月營收')

# --- Conditions ---
cond1 = (revenue / revenue.shift(12) - 1) > 0.2   # YoY revenue growth > 20%
cond2 = close > close.average(20)                   # above 20-day MA

# --- Position ---
position = cond1 & cond2

# --- Backtest config (read by headless_backtest.py) ---
RESAMPLE = 'M'
```

---

## Tips for Best Results

- **Be specific** when asking Claude for strategies. Include the signal logic, rebalance frequency, and max stock count.
- **Iterate on MDD**: If max drawdown is too high, ask Claude to add a market filter (e.g., "加上大盤月線濾網").
- **Check field names**: When Claude uses a data field you haven't seen before, verify it with `python tools/search_db.py`.
- **Keep strategies local**: The `strategies/` folder is git-ignored by design. If you want to back up strategies, use a private repo or local archive.

---

## Resources

- [FinLab Official Docs](https://doc.finlab.tw)
- [FinLab Database Browser](https://ai.finlab.tw/database)
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [FinLab Discord](https://discord.gg/tAr4ysPqvR)
