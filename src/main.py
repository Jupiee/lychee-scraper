from apscheduler.schedulers.asyncio import AsyncIOScheduler

from modules.myrient import Myrient
from modules.edge_emulation import EdgeEmulation
from modules.nopaystation import NoPayStation
from modules.database import collection

import time
import asyncio

async def mine(source):

	await source.mine()

async def main():

	sources= [Myrient(), EdgeEmulation(), NoPayStation()]
	links_to_clean= []

	for source in sources:

		response= source.check_connection()

		if response != None:

			links_to_clean.append(response)

	print("Cleaning previous data...\n\n")

	for link in links_to_clean:

		await collection.delete_many(link)

	start= time.time()

	print("Started Scraping...\n\n")

	for source in sources:

		await mine(source)

	print(f"Completed in :{round(time.time() - start)/60}minutes\nRoms indexed: {await collection.count_documents({})}")

if __name__ == '__main__':

	scheduler= AsyncIOScheduler()
	scheduler.add_job(main, "cron", hour=3, misfire_grace_time=600)
	scheduler.start()

	try:

		asyncio.get_event_loop().run_forever()

	except (KeyboardInterrupt, SystemExit):

		print("\n\nForced Exit\n")