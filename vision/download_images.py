import json 
import asyncio
from aiohttp import ClientSession
import aiofiles
import os

#Reading JSON file with 250 URLs for each of the 100 species
url_list_file = open("data/url_list_100.json")
url_list = json.load(url_list_file)

#Define functions for async HTTP GET request to download images
#This is much faster than the corresponding synchronous version
#https://progerhub.com/tutorial/downloading-random-images-using-python-requests-and-asyncio-aiohttp
async def make_request(session, url, taxon, counter):

    img_dir = "data/images"
    spec_dir = os.path.join(img_dir, taxon)

    if not os.path.exists(spec_dir):
        os.mkdir(spec_dir)

    img_path = os.path.join(spec_dir,  "{}_{}.jpeg".format(taxon, str(counter)))

    if os.path.exists(img_path):
        return

    try:
        resp = await session.request(method="GET", url=url)
    except Exception as ex:
        print(ex)
        return

    if resp.status == 200:
        async with aiofiles.open(img_path, 'wb') as f:
            await f.write(await resp.read())

async def bulk_request(url_list, taxon):
    async with ClientSession() as session:
        tasks = [make_request(session, url, taxon, count) for count, url in enumerate(url_list)]
        await asyncio.gather(*tasks)

def download_images(url_list, taxon):
    asyncio.run(bulk_request(url_list, taxon))

#Download images for each species
for taxon in url_list.keys():
    download_images(url_list[taxon], taxon)
