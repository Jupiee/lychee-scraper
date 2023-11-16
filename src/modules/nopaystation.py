from selectolax.lexbor import LexborHTMLParser
import httpx

from modules.game_item import Item
from modules.database import collection

import asyncio

class NoPayStation:

    def __init__(self):

        self.base_url= "https://nopaystation.com"

        self.urls= {

            "PS1": f"{self.base_url}/search?query=&platform=psx&category=game&limit=100&orderBy=completionDate&sort=DESC&missing=Hide",
            "PS3": f"{self.base_url}/search?query=&platform=ps3&category=game&limit=100&orderBy=completionDate&sort=DESC&missing=Hide",
            "PSP": f"{self.base_url}/search?query=&platform=psp&category=game&limit=100&orderBy=completionDate&sort=DESC&missing=Hide",
            "PSV": f"{self.base_url}/search?query=&platform=psv&category=game&limit=100&orderBy=completionDate&sort=DESC&missing=Hide"

        }

        self.timeout= httpx.Timeout(connect= None, read= None, write= None, pool= None)

        self.client_session= httpx.AsyncClient(timeout= self.timeout)

    def check_connection(self):

        try:

            response= httpx.Client().get(self.base_url)

            return True

        except httpx.ConnectTimeout:

            return None

    async def scrape_table(self, platform, url):

        count= 1

        response= await self.client_session.get(url)
        
        parser= LexborHTMLParser(response.text)

        table= parser.css_first("tbody").css("tr")

        while table != []:
            
            for row in table:

                sub_url= row.css_first("td").css_first("a").attrs["href"]

                inner_response= await self.client_session.get(f"{self.base_url}{sub_url}")

                sub_parser= LexborHTMLParser(inner_response.text)

                h4_tag= sub_parser.css_first("h4")

                if h4_tag:

                    title= h4_tag.text()
                    file_size= sub_parser.css_first("input#prettySize").attrs["value"]
                    download_link= sub_parser.css_first("input#pkg").attrs["value"]

                    game= Item(title, file_size, "-", platform, download_link)

                    await collection.insert_one(game.__dict__)

            count+= 1

            await asyncio.sleep(10)

            next_response= await self.client_session.get(url + f"&page={count}")

            parser= LexborHTMLParser(next_response.text)

            table= parser.css_first("tbody").css("tr")

    async def mine(self):

        print("Scraping NoPayStation...\n\n")

        tasks= []

        for platform, url in self.urls.items():
             
            tasks.append(self.scrape_table(platform, url))

        await asyncio.gather(*tasks)

        await self.client_session.aclose()