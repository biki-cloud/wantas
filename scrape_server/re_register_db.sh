#!/bin/sh

# セブンイレブン、ファミリーマート、ローソンの商品情報をスクレイピングし、
# database/db.sqliteに再登録する

echo "python3 util.py"
$(python3 util.py)

# echo "python3 store/familymart.py"
# python3 store/familymart.py

# echo "python3 store/seveneleven.py"
# python3 store/seveneleven.py

echo "python3 store/lawson.py"
python3 store/lawson.py

# echo "mv product_familymart.json database/"
# mv product_familymart.json database/

# echo "mv product_seveneleven.json database/"
# mv product_seveneleven.json database/

echo "mv product_lawson.json database/"
mv product_lawson.json database/

