from selectolax.lexbor import LexborHTMLParser
import httpx

from modules.game_item import Item
from modules.database import collection

import asyncio
import os.path
import json

class Myrient:

    def __init__(self):

        source_file= open(os.path.dirname(__file__) + "/../sources.json")

        self.base_url= json.load(source_file)["Myrient"]

        source_file.close()

        self.timeout= httpx.Timeout(connect= None, read= None, write= None, pool= None)

        self.client_session= httpx.AsyncClient(timeout= self.timeout)

    def check_connection(self):

        try: 

            response= httpx.Client().get("https://myrient.erista.me/files/")

            return True

        except httpx.ConnectTimeout:
                
            return None

    async def scrape_table(self, platform, url):

        response= await self.client_session.get(url)

        parser= LexborHTMLParser(response.text)

        rows= parser.css_first("tbody").css("tr")[1:]

        for row in rows:

            data= row.css("td")

            anchor_tag= data[0].css_first("a")

            game= Item(anchor_tag.text().strip(".zip"), data[1].text(), platform, self.base_url[platform] + anchor_tag.attrs["href"])

            await collection.insert_one(game.__dict__)

    async def mine(self):

        print("Scraping Myrient...\n\n")

        tasks= []

        for platform, url in self.base_url.items():

            tasks.append(self.scrape_table(platform, url))
        
        await asyncio.gather(*tasks)

        await self.client_session.aclose()
