## OLX Brazil Estate Listing Crawler
Crawls Real Estate information from OLX Brazil and stores data in JSON and SQLite.

## Result sample
![Sample output data](https://i.imgur.com/qxuFo0m.jpg)

### Dependencies
Python3.6, virtualenv (optional), sqlite3

### Setting up
- Install Python dependencies by running `pip install -r requirements.txt`
- Run `python scripts/setup_db.py`
### Running the crawler
- Run `./scripts/crawl.sh`
- Check output.json and olx.db, in the root directory of this project.
