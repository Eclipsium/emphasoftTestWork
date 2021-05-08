import asyncio
import os
import aiofiles
import aiohttp

from CONSTANTS import CONCURRENCY, BASE_DIR

count = 0


def download_file_service(items):
    global count
    os.makedirs(BASE_DIR, exist_ok=True)

    # FastAPI use asyncio main thread. We need create new event_loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    sema = asyncio.BoundedSemaphore(CONCURRENCY)

    async def fetch_file(item):
        global count
        os.makedirs(f'{BASE_DIR}/{item["form_number"]}/', exist_ok=True)
        filename = os.path.abspath(f'{BASE_DIR}/'
                                   f'{item["form_number"]}/'
                                   f'{item["form_number"]}-'
                                   f'{item["min_year"]}'
                                   f'.pdf')
        async with sema, aiohttp.ClientSession() as session:
            async with session.get(item['download_pdf']) as response:
                assert response.status == 200
                payload = await response.read()
                print(f'Start download \t\t{item["form_title"]} - {item["min_year"]}')

        async with aiofiles.open(filename, "wb") as outfile:
            await outfile.write(payload)
            print(f'Download complete \t{item["form_title"]} - {item["min_year"]}')

        count += 1

    tasks = [loop.create_task(fetch_file(url)) for url in items]
    loop.run_until_complete(asyncio.wait(tasks))

    print(f'\nAll tasks DONE!\nFetching {count} files')
    count = 0

    loop.close()
