# Data Catalog — 台股 FinLab 資料字典

> **使用規則:** 需要資料欄位時，先在此查詢正確字串。
> 若此字典沒有，執行 `python tools/search_db.py <關鍵字>` 獲取正確字串。

---

## 價格資料 `price:`

| 資料字串 | 說明 |
|----------|------|
| `price:收盤價` | 每日收盤價（還原權值） |
| `price:開盤價` | 每日開盤價 |
| `price:最高價` | 每日最高價 |
| `price:最低價` | 每日最低價 |
| `price:成交量` | 每日成交量（張） |
| `price:成交金額` | 每日成交金額（元） |

---

## 基本面資料 `fundamental_features:`

| 資料字串 | 說明 |
|----------|------|
| `fundamental_features:本益比` | PE Ratio |
| `fundamental_features:股價淨值比` | PB Ratio |
| `fundamental_features:殖利率` | 現金殖利率 (%) |
| `fundamental_features:EPS` | 每股盈餘 |

---

## 財務報表 `financial_statement:`

| 資料字串 | 說明 |
|----------|------|
| `financial_statement:營業收入` | 單季營業收入（千元） |
| `financial_statement:營業利益` | 單季營業利益（千元） |
| `financial_statement:稅後淨利` | 單季稅後淨利（千元） |
| `financial_statement:每股盈餘` | 單季 EPS |
| `financial_statement:營業毛利` | 單季毛利（千元） |

---

## 月營收 `monthly_revenue:`

| 資料字串 | 說明 |
|----------|------|
| `monthly_revenue:當月營收` | 當月營業收入（千元） |
| `monthly_revenue:上月營收` | 上月營業收入（千元） |
| `monthly_revenue:去年同月營收` | 去年同月營業收入（千元） |
| `monthly_revenue:單月營收年增率` | 月營收 YoY (%) |
| `monthly_revenue:累計營收` | 年累計營收（千元） |

---

## 籌碼資料 `chip:`

| 資料字串 | 說明 |
|----------|------|
| `chip:外資買賣超` | 外資單日買賣超（張） |
| `chip:投信買賣超` | 投信單日買賣超（張） |
| `chip:自營商買賣超` | 自營商單日買賣超（張） |
| `chip:三大法人買賣超` | 三大法人合計買賣超（張） |

---

## 技術指標 `technical:`

| 資料字串 | 說明 |
|----------|------|
| `technical:RSI` | RSI (14日) |
| `technical:MACD` | MACD 值 |
| `technical:布林通道上軌` | Bollinger Band 上軌 |
| `technical:布林通道下軌` | Bollinger Band 下軌 |

---

> **提醒:** 上表為常用欄位，實際可用欄位以 FinLab 資料庫為準。
> 不確定時執行: `python tools/search_db.py <關鍵字>`
