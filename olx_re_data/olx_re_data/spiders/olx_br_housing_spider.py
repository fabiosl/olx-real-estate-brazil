import re
import scrapy
import sqlite3
import os
import datetime

PAGES_TO_CRAWL = 100

class OLXHousingListSpider(scrapy.Spider):
    name = "olx_br_housing"
    
    base_urls = ["https://pb.olx.com.br/paraiba/joao-pessoa/imoveis/venda/apartamentos?f=a&sd=4838&sd=4812&sd=4821", 
                 "https://rn.olx.com.br/rio-grande-do-norte/natal/ponta-negra/imoveis/venda/apartamentos"]


   # Generate start urls from base URL
    start_urls = []

    for base_url in base_urls:
        if "?" not in base_url: 
            base_url += "?" 

        start_urls += [base_url + "&o=" + str(index) for index in range(1,PAGES_TO_CRAWL+1)]
    
    def parse_listing(self, listing):
        listing_name = unicode(listing.css("h2.OLXad-list-title::text").extract_first()).strip()
        listing_price = unicode(listing.css("p.OLXad-list-price::text").extract_first()).strip()
        listing_price = ''.join(["" + unicode(elem) for elem in re.findall(r'\d+', listing_price)])

        listing_id = unicode(listing.xpath("@data-lurker_list_id").extract_first()).strip()
        listing_url = unicode(listing.xpath("@href").extract_first()).strip()
        listing_details = unicode(' '.join(listing.css("p.detail-specific::text").extract())).strip()
        listing_region = unicode(' '.join(listing.css("p.detail-region::text").extract())).strip()

        listing_sq_meters = None
        listing_condominio = None
        listing_rooms = None
        listing_parking_spaces = None

        for detail in listing_details.split("|"):
            if ' m' in detail: 
                listing_sq_meters = re.findall(r'\d+', detail)[0]
            elif "Condom" in detail: 
                listing_condominio = re.findall(r'\d+', detail)[0]
            elif "quarto" in detail:
                listing_rooms = re.findall(r'\d+', detail)[0]
            elif "vaga" in detail:
                listing_parking_spaces = re.findall(r'\d+', detail)[0]
        
        retrieved_date = datetime.datetime.now().strftime("%Y-%m-%d")
        

        listing = (
            listing_name, 
            listing_price, 
            listing_id, 
            listing_url,
            listing_details, 
            listing_region, 
            retrieved_date, 
            listing_sq_meters, 
            listing_condominio, 
            listing_parking_spaces, 
            listing_rooms
        )

        # Remove duplicate spaces on each item
        listing = tuple([(" ".join(unicode(item).split())) for item in list(listing)])

        return listing

    # If you're dealing with a huge amount of data, you should insert in batch
    def inset_into_db(self, listing_tuple):
        conn = sqlite3.connect('../olx.db')
        c = conn.cursor()
        c.execute('''INSERT INTO listings
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', listing_tuple)
        conn.commit()
        conn.close()


    def parse(self, response):
        for listing in response.css("div.section_OLXad-list li.item a.OLXad-list-link"):
            listing_tuple = self.parse_listing(listing)
            self.inset_into_db(listing_tuple)

            yield {
                'listing_name': listing_tuple[0],
                'listing_price': listing_tuple[1],
                'listing_id': listing_tuple[2],
                'listing_url': listing_tuple[3],
                'listing_details': listing_tuple[4],
                'listing_region': listing_tuple[5],
                'retrieved_date': listing_tuple[6], 
                'listing_sq_meters': listing_tuple[7],
                'listing_condominio': listing_tuple[8],
                'listing_parking_spaces': listing_tuple[9],
                'listing_rooms': listing_tuple[10]
            }