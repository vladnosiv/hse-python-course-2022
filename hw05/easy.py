import argparse
import asyncio
import ssl
from pathlib import Path

import aiofiles as aiofiles
import aiohttp as aiohttp


async def download_pic(session: aiohttp.ClientSession,
                       url: str,
                       path_to_save: Path):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        if response.status == 200:
            async with aiofiles.open(path_to_save, 'wb') as f:
                await f.write(await response.read())


async def download_pics(url: str,
                        n_pics: int,
                        download_path: str):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[
            download_pic(session, url, Path(download_path) / f'image{i}.png')
            for i in range(n_pics)
        ])


if __name__ == '__main__':
    URL = 'https://picsum.photos/200'
    parser = argparse.ArgumentParser(description=f'Download random pictures from {URL}')
    parser.add_argument('download_path', metavar='Dir', type=str, nargs=1,
                        help='Download directory')
    parser.add_argument('n_pics', metavar='N', type=int, nargs=1,
                        help='Number of pictures to download')
    args = parser.parse_args()
    n_pics = args.n_pics[0]
    download_path = args.download_path[0]

    asyncio.run(download_pics(URL, n_pics, download_path))




