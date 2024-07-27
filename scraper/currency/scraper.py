from dataclasses import dataclass
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.db.models import QuerySet
from fake_useragent import UserAgent
from main.models import Currency, CurrencyRateHistory
from django.db import IntegrityError, transaction

@dataclass
class RawCurrencyData:
    symbol: str
    name: str
    per_USD: str


class CurrencyScraper:

    def __init__(self, *, currency_symbol: str = None, date: datetime = None, url: str = None):

        self.url: str = url or 'https://www.xe.com/currencytables/'
        self.date: datetime.date = date or datetime.today()
        self.params = {
            'from': currency_symbol or 'USD',
            'date': self.date.strftime('%Y-%m-%d'),
        }

        ua = UserAgent()
        self.headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self.url,
            'Cache-Control': 'max-age=0'
        }

    def get_raw_data(self) -> list[RawCurrencyData] | list:
        response = requests.get(url=self.url, params=self.params, headers=self.headers)

        if response.status_code != 200:
            return []

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find(id='table-section').find('table')
            if table is None:
                return []
        except (UnicodeDecodeError, AttributeError, TypeError):
            return []
        except Exception:
            return []

        data = []
        rows = table.find_all('tr')
        for row in rows:
            try:
                a = row.find('th').find('a')
                cells = row.find_all('td')
            except AttributeError:
                continue

            if not a or len(cells) < 2:
                continue

            symbol = a.get_text(strip=True)
            name = cells[0].get_text(strip=True)
            per_usd = cells[1].get_text(strip=True)
            data.append(RawCurrencyData(symbol=symbol, name=name, per_USD=per_usd))

        return data

    def update_or_create_currencies(self, raw_data_list: list[RawCurrencyData]):

        if not raw_data_list:
            raw_data_list = self.get_raw_data()

        existing_currencies = Currency.objects.in_bulk(field_name='code')

        new_currencies = []
        for raw_data in raw_data_list:
            if not raw_data.symbol in existing_currencies and len(raw_data.symbol) <= 3:
                new_currencies.append(Currency(code=raw_data.symbol))
        try:
            with transaction.atomic():
                Currency.objects.bulk_create(new_currencies)
            return True
        except Exception:
            return False

    def write_rate_history(self) -> QuerySet:
        raw_data_list = self.get_raw_data()
        self.update_or_create_currencies(raw_data_list)

        currencies = Currency.objects.all()
        data_list = [CurrencyRateHistory(currency=currency, per_usd=raw_data.per_USD, date=self.date) for raw_data in raw_data_list for
                             currency in currencies if currency.code == raw_data.symbol]


        try:
            with transaction.atomic():
                data_list = CurrencyRateHistory.objects.bulk_create(data_list)
        except IntegrityError:
            for data in data_list:
                try:
                    data.save()
                except IntegrityError:
                    continue
            data_list = CurrencyRateHistory.objects.filter(date=self.date).all()

        return data_list


