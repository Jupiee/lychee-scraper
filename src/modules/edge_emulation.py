from selectolax.lexbor import LexborHTMLParser
import httpx

from modules.game_item import Item
from modules.database import collection

import asyncio

class EdgeEmulation:

    def __init__(self):

        self.base_url= "https://edgeemu.net"
        self.letters= "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.platforms= ["gba", "gc", "gbc", "nds", "vb", "n64", "nes", "snes"]

        self.formatted_platforms= {"gba": "Gameboy Advance",
                                   "gc": "Nintendo GameCube",
                                   "gbc": "Gameboy Color",
                                   "nds": "Nintendo DS",
                                   "vb": "Virtual Boy",
                                   "n64": "Nintendo 64",
                                   "nes": "NES",
                                   "snes": "SNES"}

        self.timeout= httpx.Timeout(connect= None, read= None, write= None, pool= None)
        self.client_session= httpx.AsyncClient(timeout= self.timeout)

    def check_connection(self):

        try:

            response= httpx.Client().get(self.base_url)

            return True

        except httpx.ConnectTimeout:

            return None

    async def scrape_table(self, platform, letter):

        if letter == "#":

            url= f"{self.base_url}/browse-{platform}-num.htm"

        else:

            url= f"{self.base_url}/browse-{platform}-{letter}.htm"

        response= await self.client_session.get(url)

        parser= LexborHTMLParser(response.text)

        table_body= parser.css_first("tbody")

        if table_body is not None:

            rows= table_body.css("tr")[1:]

            for row in rows:

                data= row.css("td")

                anchor_tag= data[0].css_first("a")

                game= Item(anchor_tag.text(), data[1].text(), self.formatted_platforms[platform], f"{self.base_url}/{anchor_tag.attrs['href']}")

                await collection.insert_one(game.__dict__)

    async def mine(self):

        print("Scraping EdgeEmu...\n\n")

        tasks= []

        for platform in self.platforms:

            for letter in self.letters:

                tasks.append(self.scrape_table(platform, letter))
        
        await asyncio.gather(*tasks)

        await self.client_session.aclose()