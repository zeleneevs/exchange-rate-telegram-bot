import datetime
from contextlib import asynccontextmanager
import aiohttp

URL = 'https://api.exchangeratesapi.io'
TIMEOUT = aiohttp.ClientTimeout(total=3)


class ERException(Exception):
    pass


@asynccontextmanager
async def er_session():
    session = aiohttp.ClientSession(timeout=TIMEOUT, raise_for_status=True)
    try:
        yield session
    except aiohttp.ClientError:
        raise ERException
    finally:
        await session.close()


async def latest(base='USD'):
    url = f'{URL}/latest?base={base}'

    async with er_session() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def history(base='USD', symbols='CAD', delta=7):
    end_at = datetime.date.today()
    start_at = end_at - datetime.timedelta(delta)
    end_at = end_at.isoformat()
    start_at = start_at.isoformat()
    url = f'{URL}/history?start_at={start_at}&end_at={end_at}&base={base}&symbols={symbols}'

    async with er_session() as session:
        async with session.get(url) as resp:
            return await resp.json()
