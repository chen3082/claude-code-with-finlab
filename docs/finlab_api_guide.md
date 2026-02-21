# FinLab API Guide（官方文檔整合版）

> **來源:** https://doc.finlab.tw
> **重要:** 寫任何策略 Code 前必須先閱讀本文件。嚴禁捏造不存在的 API。

---

## 1. 初始化與登入

```python
import os
from dotenv import load_dotenv
import finlab
from finlab import data

load_dotenv()
finlab.login(os.getenv("FINLAB_API_TOKEN"))
```

---

## 2. 資料取得 `finlab.data`

### 2.1 `data.get()` — 下載資料

```python
close   = data.get('price:收盤價')
pe      = data.get('price_earning_ratio:本益比')
revenue = data.get('monthly_revenue:當月營收')
```

- 回傳 **FinlabDataFrame**（pandas DataFrame 的擴充版）
- 縱軸：交易日期；橫軸：股票代號

**參數：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `dataset` | 資料表名稱，格式 `"table:column"` | 必填 |
| `save_to_storage` | 是否快取到本地 | `True` |
| `force_download` | 強制從雲端下載 | `False` |

### 2.2 `data.search()` — 搜尋可用欄位

```python
data.search('收盤')           # 搜尋含「收盤」的欄位
data.search('close', market='us')  # 搜尋美股欄位
data.search()                  # 列出全部
```

**參數：**
- `keyword`：搜尋關鍵字（不分大小寫），為 `None` 時列出全部
- `market`：`'tw'`（預設）、`'us'`、`'all'`

### 2.3 `data.universe()` — 限定股票範圍

```python
# 只取上市股票
with data.universe(market='TSE'):
    close = data.get('price:收盤價')

# 指定產業
with data.universe(category=['水泥工業', '食品工業']):
    close = data.get('price:收盤價')

# 排除產業
with data.universe(market='TSE_OTC', exclude_category=['金融']):
    price = data.get('price:收盤價')
```

**market 選項：** `ALL` / `TSE` / `OTC` / `TSE_OTC` / `ETF`

### 2.4 `data.indicator()` — 技術指標

```python
# RSI
rsi = data.indicator('RSI', timeperiod=14)

# KD 值（回傳兩個 DataFrame）
k, d = data.indicator('STOCH')

# 計算所有股票的 MACD
macd = data.indicator('MACD')
```

### 2.5 全域設定

```python
# 限制資料範圍（加快速度、節省記憶體）
data.truncate_start = '2020-01-01'
data.truncate_end   = '2023-12-31'

# 強制從雲端下載
data.force_cloud_download = True
```

---

## 3. FinlabDataFrame — 核心選股工具

> **關鍵規則：FinlabDataFrame 會自動對齊不同頻率資料（日/月/季），嚴禁使用 `pd.merge` / `pd.concat`**

### 3.1 運算符號

| 類型 | 運算符 |
|------|--------|
| 算術 | `+` `-` `*` `/` |
| 比較 | `>` `>=` `==` `<` `<=` |
| 邏輯 | `&`（AND）`|`（OR）`~`（NOT） |

```python
close = data.get('price:收盤價')
ma20  = close.average(20)

# 自動對齊不同頻率資料
revenue = data.get('monthly_revenue:當月營收')
position = (close > ma20) & (revenue > 1e8)   # 日頻 & 月頻，自動對齊
```

### 3.2 移動平均 `average(n)`

```python
sma20    = close.average(20)
position = close > sma20
```

### 3.3 選股排名

```python
# 選每日 ROA 最大的 10 檔
roa = data.get('fundamental_features:ROA稅後息前')
position = roa.is_largest(10)

# 選每日股價淨值比最小的 10 檔
pb = data.get('price_earning_ratio:股價淨值比')
position = pb.is_smallest(10)

# 橫截面百分位排名
cap_rank = data.get('etl:market_value').rank(pct=True, axis=1)
position = cap_rank > 0.7   # 市值前 30%
```

### 3.4 趨勢判斷

```python
close.rise(3)           # 連續 3 日上漲
close.fall(2)           # 連續 2 日下跌
(close > ma20).sustain(5)     # 連續 5 日站穩均線
(close > ma20).sustain(3, 2)  # 3 日中有 2 日站穩
```

### 3.5 進出場控制 `hold_until()`

**最核心的策略語法：**

```python
buy  = close > close.average(5)
sell = close < close.average(20)

position = buy.hold_until(sell)
```

**進階參數：**

| 參數 | 說明 | 範例 |
|------|------|------|
| `stop_loss` | 停損比例 | `stop_loss=0.1` → 跌 10% 出場 |
| `take_profit` | 停利比例 | `take_profit=0.2` → 漲 20% 出場 |
| `nstocks_limit` | 最多持有股數 | `nstocks_limit=10` |
| `rank` | 選股優先排序 | `rank=-pb`（pb 越小越優先） |

```python
pb = data.get('price_earning_ratio:股價淨值比')

position = (close > close.average(20)).hold_until(
    close < close.average(60),
    nstocks_limit=10,
    stop_loss=0.1,
    rank=-pb
)
```

### 3.6 進出場時點

```python
position.is_entry()   # 取進場時點（False→True 轉變）
position.is_exit()    # 取出場時點（True→False 轉變）
```

### 3.7 產業分析

```python
# 產業中性化
factor = data.get('fundamental_features:股東權益報酬率')
neutral = factor.neutralize_industry()
position = neutral.is_largest(30)

# 多因子中性化
size = data.get('etl:market_value')
neutralized = factor.neutralize(size)

# 產業分群
pe = data.get('price_earning_ratio:股價淨值比')
pe.groupby_category().mean()['半導體'].plot()

# 產業內排名
pe_rank = pe.industry_rank()
```

### 3.8 輔助方法

```python
# 財報索引轉為公告截止日
data.get('financial_statement:現金及約當現金').index_str_to_date()

# 每日橫截面分位數值
close.quantile_row(0.9)
```

---

## 4. 回測 `finlab.backtest.sim()`

```python
from finlab.backtest import sim

report = sim(
    position,
    resample='M',          # 調倉頻率
    position_limit=0.1,    # 單股持倉上限 10%
    fee_ratio=1.425/1000,  # 手續費
    tax_ratio=3/1000,      # 交易稅
    name='我的策略',
    upload=True
)

report.display()
```

### 4.1 `sim()` 完整參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `position` | 買賣訊號 DataFrame（True/False） | **必填** |
| `resample` | 調倉週期：`'D'`/`'W'`/`'M'`/`'Q'` | `None` |
| `trade_at_price` | 交易價格基準：`'close'`/`'open'` | `'close'` |
| `position_limit` | 單股持倉上限（0~1） | `1` |
| `fee_ratio` | 手續費率 | `0.001425` |
| `tax_ratio` | 交易稅率 | `0.003` |
| `stop_loss` | 停損 | `None` |
| `take_profit` | 停利 | `None` |
| `trail_stop` | 移動停損 | `None` |
| `fast_mode` | 快速模式（跳過部分計算） | `False` |
| `upload` | 上傳至雲端 | `True` |

### 4.2 `resample` 說明

| 值 | 說明 |
|----|------|
| `'D'` | 每日調倉 |
| `None` | 僅清單改變時調倉 |
| `'W'` | 每週調倉 |
| `'W-Wed'` | 每週三調倉 |
| `'M'` | 每月調倉 |
| `'Q'` | 每季調倉 |

### 4.3 Report 常用方法

```python
report.display()                  # 視覺化績效報告
report.get_trades()               # 取得交易紀錄
report.get_stats()                # 取得 KPI（CAGR, MDD, Sharpe...）
report.display_mae_mfe_analysis() # 波動分析
```

### 4.4 避免未來函數

```python
# ❌ 錯誤：當日收盤判斷並以收盤交易（未來函數）
report = sim(position, trade_at_price='close')

# ✅ 正確：以隔日開盤價交易
report = sim(position, trade_at_price='open')
```

---

## 5. 完整策略範本

```python
import os
from dotenv import load_dotenv
import finlab
from finlab import data
from finlab.backtest import sim

load_dotenv()
finlab.login(os.getenv("FINLAB_API_TOKEN"))

# --- 資料 ---
close     = data.get('price:收盤價')
marketcap = data.get('etl:market_value')
revenue   = data.get('monthly_revenue:當月營收')
roe       = data.get('fundamental_features:股東權益報酬率')

# --- 選股條件 ---
cond1 = marketcap.is_smallest(100)                          # 小型股
cond2 = (revenue.average(3) / revenue.average(12)) > 1.2   # 營收成長
cond3 = roe.rank(pct=True, axis=1) > 0.7                   # ROE 前 30%
cond4 = (close > close.average(20)).sustain(3)              # 站穩均線

# --- 進出場 ---
position = (cond1 & cond2 & cond3 & cond4).hold_until(
    close < close.average(60),
    nstocks_limit=20,
    stop_loss=0.1
)

# --- 回測 ---
report = sim(position, resample='M', position_limit=0.05)
report.display()
```

---

## 6. 常見錯誤排解

| 錯誤 | 原因 | 解法 |
|------|------|------|
| `KeyError` | 欄位名稱錯誤 | 執行 `python tools/search_db.py <關鍵字>` |
| Empty DataFrame | 篩選條件過嚴 | 放寬條件或使用 `is_largest(N)` |
| 回測無交易紀錄 | `position` 全為 False | 檢查邏輯運算子 |
| 資料對齊錯誤 | 使用了 `pd.merge` | 改用 FinlabDataFrame 運算符號 |
| API Token 失敗 | Token 錯誤或過期 | 確認 `.env` 設定 |
