# import sys
# sys.path.append('..')
import asyncio
import tornado
from tornado.httpclient import AsyncHTTPClient

from produce import send


async def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
    except Exception as e:
        print(f"Error: {e}")
    else:
        return response.body


async def main():
    result = await fetch_coroutine('https://reqres.in/api/users')
    data = tornado.escape.json_decode(result)
    send(data)

if __name__ == "__main__":
    asyncio.run(main())
