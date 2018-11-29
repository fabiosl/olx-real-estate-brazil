echo "Recreating db..."
rm olx.db
python scripts/setup_db.py
cd olx_re_data
scrapy crawl olx_br_housing -o output.json
echo "Done!"
cd ..