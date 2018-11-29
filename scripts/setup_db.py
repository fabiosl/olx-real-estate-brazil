import sqlite3

conn = sqlite3.connect('olx.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE listings
             (
             title text,  
             price real, 
             ad_id integer primary key,
             listing_url text,
             listing_details text,
             listing_region text,
             retrieved_date text,
             listing_sq_meters text,
             listing_condominio text,
             listing_parking_spaces text,
             listing_rooms text
             )''')

conn.commit()
conn.close()