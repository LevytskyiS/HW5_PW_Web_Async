import time
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta


class GettCurrency(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.today = datetime.today()
        self.formatted_date = self.today.strftime("%d.%m.%Y")
        self.pb_url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={self.formatted_date}"

    @abstractmethod
    def get_currency():
        pass


class GetUSD(GettCurrency):
    async def get_currency(self, session, days):
        start = time.time()
        data = {}

        while days != 0:

            async with session.get(self.pb_url) as response:
                print(f"Start getting USD")
                result = await response.json()
                ex_rates = result["exchangeRate"]
                for rate in ex_rates:
                    if "USD" in rate.values():
                        data.update({f"{self.formatted_date}": rate})
                self.today -= timedelta(days=1)
                self.formatted_date = self.today.strftime("%d.%m.%Y")
                self.pb_url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={self.formatted_date}"
                days -= 1
                print(f"Done USD in {time.time() - start}")
        return data


class GetEUR(GettCurrency):
    async def get_currency(self, session, days):
        start = time.time()
        data = {}

        while days != 0:

            async with session.get(self.pb_url) as response:
                print(f"Start getting EUR")
                result = await response.json()
                ex_rates = result["exchangeRate"]
                for rate in ex_rates:
                    if "EUR" in rate.values():
                        data.update({f"{self.formatted_date}": rate})
                self.today -= timedelta(days=1)
                self.formatted_date = self.today.strftime("%d.%m.%Y")
                self.pb_url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={self.formatted_date}"
                days -= 1
                print(f"Done EUR in {time.time() - start}")
        return data
