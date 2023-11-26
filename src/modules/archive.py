from selectolax.lexbor import LexborHTMLParser
import httpx

from modules.game_item import Item
from modules.database import collection

import asyncio
import json

class Archive:

    def __init__(self):

        source_file= open("F:/Code treasure/Lychee engine/backend/lychee-scraper/src/sources.json")

        self.urls= json.load(source_file)["Archive"]

        source_file.close()

        self.timeout= httpx.Timeout(connect= None, read= None, write= None, pool= None)

        self.client_session= httpx.AsyncClient(timeout= self.timeout)

    def check_connection(self):

        try:

            response= httpx.Client().get("https://archive.org")

            return True

        except httpx.ConnectTimeout:

            return None
        
    async def scrape_table(self, platform, url):

        response= await self.client_session.get(url)

        parser= LexborHTMLParser(response.text)

        table= parser.css_first("table.directory-listing-table > tbody").css("tr")[1:]

        for row in table:

            name= row.css_first("td").css_first("a").text()

            if name.endswith(".iso") or name.endswith(".zip"):

                link= row.css_first("td").css_first("a").attrs["href"]

                download_link= f"{url}/{link}"

                size= row.css("td")[2].text()

                item= Item(name, size, "-", platform, download_link)

                await collection.insert_one(item.__dict__)
    
    async def mine(self):

        print("Scraping Archive.org...\n\n")

        tasks= []

        for platform, url_list in self.urls.items():

            for url in url_list:

                tasks.append(self.scrape_table(platform, url))

        await asyncio.gather(*tasks)

        await self.client_session.aclose()