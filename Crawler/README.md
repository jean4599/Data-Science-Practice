# 爬蟲練習 PYTHON3.6
爬2017年ptt beauty版的文章
包含四個主要的function:
1. **python3 crawler crawl**: 爬2017年的所有文章
2. **python3 crawler push *start_date end_date***: 計算指定日期區間的推噓文數量、找前十名推文最多、前十名虛文最多的userid
3. **python3 crawler popular *start_date end_date***: 找指定日期區間的爆文，數爆文數量、輸出文章的圖片URL
4. **python3 crawler keyword *query_keyword start_date end_date***: 找指定日期區間含有query_keyword的文章，數符合條件的文章數量、輸出文章的圖片URL

# Require packages:
### Requests
pip install requests

### BeautifulSoup4
pip install beautifulsoup4

### Fire
pip install fire
