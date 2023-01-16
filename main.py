import asyncio
import aiohttp
import sys
import time
from get_usd_eur import GetUSD, GetEUR, PrepareFinalResult


DAYS = [day for day in range(11)]


async def main():

    async with aiohttp.ClientSession() as session:

        try:
            search_days = int(sys.argv[1])
            if search_days in DAYS:
                usd = asyncio.create_task(GetUSD().get_currency(session, search_days))
                eur = asyncio.create_task(GetEUR().get_currency(session, search_days))

                tasks = [usd, eur]
                responses = await asyncio.gather(*tasks)
                result = PrepareFinalResult().prepare_final_result(responses)

                return result

            else:
                return "You can check the currency of a maximum period of 10 days."

        except IndexError as error:
            print(error)
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    start = time.time()
    currency = asyncio.run(main())
    print(time.time() - start)
    print(currency)
