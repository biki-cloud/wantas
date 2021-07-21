#!/bin/sh

# セブンイレブン、ファミリーマート、ローソンの商品情報をスクレイピングし、
# database/products_json/db.sqliteに再登録する
echo "start $(date)"

echo "python3 util.py"
$(python3 util.py)

# echo "python3 store/familymart.py"
# python3 store/familymart.py

rm -fr database/products_json/*_product_familymart.json
rm -fr database/products_json/*_product_seveneleven.json
rm -fr database/products_json/*_product_lawson.json

mv database/products_json/product_familymart.json database/products_json/$(date "+%Y%m%d")_product_familymart.json
mv database/products_json/product_seveneleven.json database/products_json/$(date "+%Y%m%d")_product_seveneleven.json
mv database/products_json/product_lawson.json database/products_json/$(date "+%Y%m%d")_product_lawson.json

echo "cp store/product_familymart.json database/products_json/product_familymart.json"
cp store/product_familymart.json database/products_json/product_familymart.json
#echo "python3 store/familymart.py database/products_json/product_familymart.json"
#python3 store/familymart.py database/products_json/product_familymart.json

echo "python3 store/seveneleven.py database/products_json/product_seveneleven.json"
python3 store/seveneleven.py database/products_json/product_seveneleven.json

echo "python3 store/lawson.py database/products_json/product_lawson.json"
python3 store/lawson.py database/products_json/product_lawson.json


echo "python3 database/products_json/db.py database/products_json/product_seveneleven.json database/products_json/product_lawson.json database/products_json/product_familymart.json"
python3 database/db.py database/products_json/product_seveneleven.json database/products_json/product_lawson.json database/products_json/product_familymart.json

echo "end $(date)"
