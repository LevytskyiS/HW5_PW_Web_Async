import time
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlparse, urlunparse


class GettCurrency:
    def __init__(
        self,
        today=datetime.today(),
        api_url=f"https://api.privatbank.ua/p24api/exchange_rates?json&date=16.01.2023",
        currencies=["EUR", "USD"],
    ):

        self.EUR, self.USD, *_ = currencies
        self.today = today
        self.api_url = api_url
        self.data = []

    def change_api_query_date(self):

        parsed_url = urlparse(self.api_url)
        self.today = self.today - timedelta(days=1)
        new_query = f"{'json&date'}={self.today.strftime('%d.%m.%Y')}"
        corrected_api_url = parsed_url._replace(query=new_query)
        self.api_url = urlunparse(corrected_api_url)

    async def get_usd_eur(self, response, currency: str):

        json_data = await response.json()
        ex_rates = json_data["exchangeRate"]

        for rate in ex_rates:
            if currency in rate.values():
                self.data.append({json_data["date"]: rate})

    async def get_currency(self, session, days):

        while days != 0:

            async with session.get(self.api_url) as response:

                if response.status != 200:
                    self.data.append({str(response.status): self.api_url})

                if self.EUR == "EUR":
                    eur = asyncio.create_task(self.get_usd_eur(response, self.EUR))
                else:
                    eur = asyncio.sleep(1)

                if self.USD == "USD":
                    usd = asyncio.create_task(self.get_usd_eur(response, self.USD))
                else:
                    usd = asyncio.sleep(1)

                tasks = [eur, usd]
                await asyncio.gather(*tasks)

                self.change_api_query_date()
                days -= 1

        return self.data


class PrepareFinalResult:
    def prepare_final_result(responses: list):

        result = defaultdict(list)
        dates = []
        currencies = []
        final_result = []

        for response in responses:
            for key, value in response.items():
                val = {
                    value["currency"]: {
                        "Sale": round(value["saleRateNB"], 2),
                        "Purchase": round(value["purchaseRateNB"], 2),
                    }
                }
                dates.append(key)
                currencies.append(val)

        for d, c in zip(dates, currencies):
            result[d].append(c)

        for key, value in result.items():
            a, b, *_ = value
            dcr = {key: {"EUR": a["EUR"], "USD": b["USD"]}}
            if dcr not in final_result:
                final_result.append(dcr)

        return final_result
