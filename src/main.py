from apscheduler.schedulers.asyncio import AsyncIOScheduler

from modules.myrient import Myrient
from modules.edge_emulation import EdgeEmulation
from modules.nopaystation import NoPayStation
from modules.database import collection

import time
import asyncio

async def main():

	sources= [Myrient(), EdgeEmulation()]

	print("Cleaning previous data...\n\n")
	
	await collection.delete_many({})

	start= time.time()

	print("Started Scraping...\n\n")

	for source in sources:

		if source.check_connection():

			await source.mine()

	print(f"Completed in: {round((time.time() - start)/60)} minutes\nRoms indexed: {await collection.count_documents({})}")

if __name__ == '__main__':

	scheduler= AsyncIOScheduler()
	scheduler.add_job(main, "cron", hour=3, misfire_grace_time=600)
	scheduler.start()

	try:

		asyncio.get_event_loop().run_forever()

	except (KeyboardInterrupt, SystemExit):

		print("\n\nForced Exit\n")