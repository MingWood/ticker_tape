from aiohttp import ClientSession


async def get(url, headers=None, params=None):
    async with ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            status = response.status
            headers = response.headers
            resp = await response.text()
            return {
                'status': status,
                'headers': headers,
                'response': resp
            }


async def post(url, headers=None, params=None):
    async with ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            status = response.status
            headers = response.headers
            resp = await response.text()

            return {
                'status': status,
                'headers': headers,
                'response': resp
            }


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()

    async def example_http():
        print(await get('https://google.com'))

    loop.run_until_complete(
        example_http()
    )
