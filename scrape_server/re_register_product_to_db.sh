#!/bin/sh

# セブンイレブン、ファミリーマート、ローソンの商品情報をスクレイピングし、
# database/products_json/db.sqliteに再登録する
echo "start $(date)" >> /home/hibiki/wantas/log/scraping.log 2>&1

echo "python3 /home/hibiki/wantas/scrape_server/util/__init__.py" >> /home/hibiki/wantas/log/scraping.log 2>&1
$(python3 /home/hibiki/wantas/scrape_server/util/__init__.py)

rm -fr /home/hibiki/wantas/scrape_server/database/products_json/*_product_familymart.json >> /home/hibiki/wantas/log/scraping.log 2>&1
mv /home/hibiki/wantas/scrape_server/database/products_json/product_familymart.json /home/hibiki/wantas/scrape_server/database/products_json/$(date "+%Y%m%d")_product_familymart.json >> /home/hibiki/wantas/log/scraping.log 2>&1
echo "/home/hibiki/wantas/scrape_server/python3 store/familymart.py /home/hibiki/wantas/scrape_server/database/products_json/product_familymart.json" >> /home/hibiki/wantas/log/scraping.log 
python3 /home/hibiki/wantas/scrape_server/store/familymart.py /home/hibiki/wantas/scrape_server/database/products_json/product_familymart.json >> /home/hibiki/wantas/log/scraping.log 2>&1

rm -fr /home/hibiki/wantas/scrape_server/database/products_json/*_product_seveneleven.json >> /home/hibiki/wantas/log/scraping.log 2>&1
mv /home/hibiki/wantas/scrape_server/database/products_json/product_seveneleven.json /home/hibiki/wantas/scrape_server/database/products_json/$(date "+%Y%m%d")_product_seveneleven.json >> /home/hibiki/wantas/log/scraping.log 2>&1
echo "/home/hibiki/wantas/scrape_server/python3 store/seveneleven.py /home/hibiki/wantas/scrape_server/database/products_json/product_seveneleven.json" >> /home/hibiki/wantas/log/scraping.log
python3 /home/hibiki/wantas/scrape_server/store/seveneleven.py /home/hibiki/wantas/scrape_server/database/products_json/product_seveneleven.json >> /home/hibiki/wantas/log/scraping.log 2>&1

rm -fr /home/hibiki/wantas/scrape_server/database/products_json/*_product_lawson.json >> /home/hibiki/wantas/log/scraping.log 2>&1
mv /home/hibiki/wantas/scrape_server/database/products_json/product_lawson.json /home/hibiki/wantas/scrape_server/database/products_json/$(date "+%Y%m%d")_product_lawson.json >> /home/hibiki/wantas/log/scraping.log 2>&1
echo "python3 /home/hibiki/wantas/scrape_server/store/lawson.py /home/hibiki/wantas/scrape_server/database/products_json/product_lawson.json" >> /home/hibiki/wantas/log/scraping.log
python3 /home/hibiki/wantas/scrape_server/store/lawson.py /home/hibiki/wantas/scrape_server/database/products_json/product_lawson.json >> /home/hibiki/wantas/log/scraping.log 2>&1


echo "python3 /home/hibiki/wantas/scrape_server/database/products_json/db.py /home/hibiki/wantas/scrape_server/database/products_json/product_seveneleven.json /home/hibiki/wantas/scrape_server/database/products_json/product_lawson.json /home/hibiki/wantas/scrape_server/database/products_json/product_familymart.json" >> /home/hibiki/wantas/log/scraping.log
python3 /home/hibiki/wantas/scrape_server/database/db.py /home/hibiki/wantas/scrape_server/database/products_json/product_seveneleven.json /home/hibiki/wantas/scrape_server/database/products_json/product_lawson.json /home/hibiki/wantas/scrape_server/database/products_json/product_familymart.json >> /home/hibiki/wantas/log/scraping.log 2>&1

echo "end $(date)" >> /home/hibiki/wantas/log/scraping.log
