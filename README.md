<h1 align="center">Lychee Scraper</h1>

<p>This repository contains the source code for Lychee Scraper, used to scrape Rom links</p>
<p>The code works the same as mentioned in <a>https://lychee-engine.xyz/about</a></p>

<h3>Setup</h3>

1. Make a .env file in ```src/modules```
2. Make a MongoDB database and put your Database URI in .env ```URI= Your_database_URI```
3. Run the main file

<h3>Testing locally</h3>

1. Follow the same steps from 1 to 2 or skip if you have already done those.
2. In the main file, comment out the cron job code block and uncomment the testing code block

```python
# This is for testing purposes
asyncio.run(main())

# This is for cron job scheduling
'''scheduler= AsyncIOScheduler()
scheduler.add_job(main, "cron", hour=3, misfire_grace_time=600)
scheduler.start()

try:

    asyncio.get_event_loop().run_forever()

except (KeyboardInterrupt, SystemExit):

    print("\n\nForced Exit\n")'''
```

3. Run the main file