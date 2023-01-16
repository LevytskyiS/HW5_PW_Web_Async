from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlparse, urlunparse


class GettCurrency:

    EUR = "EUR"
    USD = "USD"
    today = datetime.today()
    api_url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date=16.01.2023"

    def change_bank_api(new_api_url):

        GettCurrency.api_url = new_api_url

    def change_api_query_date():

        parsed_url = urlparse(GettCurrency.api_url)
        new_query = f"{'json&date'}={(GettCurrency.today - timedelta(days=1)).strftime('%d.%m.%Y')}"
        corrected_api_url = parsed_url._replace(query=new_query)
        GettCurrency.api_url = urlunparse(corrected_api_url)

    async def get_currency(session, days):

        data = []

        while days != 0:

            async with session.get(GettCurrency.api_url) as response:

                if response.status != 200:
                    data.append({str(response.status): GettCurrency.api_url})

                json_data = await response.json()
                ex_rates = json_data["exchangeRate"]

                for rate in ex_rates:
                    if GettCurrency.USD in rate.values():
                        data.append({json_data["date"]: rate})
                    if GettCurrency.EUR in rate.values():
                        data.append({json_data["date"]: rate})

                GettCurrency.change_api_query_date()
                days -= 1

        return data


class PrepareFinalResult:
    def prepare_final_result(responses: list):

        result = defaultdict(list)
        dates = []
        currencies = []
        final_result = []
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
            dcr = {key: {"USD": a["USD"], "EUR": b["EUR"]}}
            if dcr not in final_result:
                final_result.append(dcr)

        return final_result
