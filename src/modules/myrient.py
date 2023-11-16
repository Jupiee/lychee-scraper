from selectolax.lexbor import LexborHTMLParser
import httpx

from modules.game_item import Item
from modules.database import collection

import asyncio

class Myrient:

    def __init__(self):

        self.base_url= {

            "PS1": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/",
            "PS2": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/",
            "PSP": "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%20Portable/",
            "Xbox": "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox/",
            "Xbox360": "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox%20360/",
            "Nintendo DS": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Decrypted)/",
            "Nintendo 3DS": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%203DS%20(Decrypted)/",
            "Nintendo GameCube": "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20[zstd-19-128k]/",
            "Nintendo Wii": "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20[zstd-19-128k]/",
            "Nintendo Wii U": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Wii%20U%20(Digital)%20(CDN)/",
            "Nintendo 64": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(BigEndian)/",
            "NES": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headered)/",
            "SNES": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/",
            "Gameboy": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/",
            "Gameboy Advance": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/",
            "Gameboy Color": "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/",

        }

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

            game= Item(anchor_tag.text().strip(".zip"), data[1].text(), data[2].text(), platform, self.base_url[platform] + anchor_tag.attrs["href"])

            await collection.insert_one(game.__dict__)

    async def mine(self):

        print("Scraping Myrient...\n\n")

        tasks= []

        for platform, url in self.base_url.items():

            tasks.append(self.scrape_table(platform, url))
        
        await asyncio.gather(*tasks)

        await self.client_session.aclose()
