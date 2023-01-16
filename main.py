import asyncio
import aiohttp
import sys
import time
import platform
from get_usd_eur import GettCurrency, PrepareFinalResult


async def find_currencies(session, days):

    futures = await GettCurrency().get_currency(session, days)

    if not futures:
        return f"No currencies have been found"

    return PrepareFinalResult.prepare_final_result(futures)


async def main():

    async with aiohttp.ClientSession() as session:

        try:
            search_days = int(sys.argv[1])
        except (IndexError, ValueError) as error:
            return error

        if 0 < search_days < 11:
            return await find_currencies(session, search_days)
        else:
            return "You can check the currency of a maximum period of 10 days."


if __name__ == "__main__":
    start = time.time()
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    currency = asyncio.run(main())
    print(time.time() - start)
    print(currency)
