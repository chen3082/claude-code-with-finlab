"""
search_db.py — 搜尋 FinLab 資料庫可用欄位

用法:
    python tools/search_db.py <關鍵字>
    python tools/search_db.py 營收
    python tools/search_db.py 外資
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

import finlab
from finlab import data

def search(keyword: str):
    finlab.login(os.getenv("FINLAB_API_TOKEN"))

    print(f"\n搜尋關鍵字: 「{keyword}」\n")
    print("-" * 50)

    results = data.search(keyword)

    if not results:
        print("找不到相關欄位，請嘗試其他關鍵字。")
        return

    for item in results:
        print(item)

    print("-" * 50)
    print(f"共找到 {len(results)} 筆結果")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python tools/search_db.py <關鍵字>")
        sys.exit(1)

    keyword = " ".join(sys.argv[1:])
    search(keyword)
