import requests

from django.conf import settings


API_URL = settings.STOCK_API_URL + '{ticker}/chart/{duration}'


def request_data(ticker, duration='1y'):
    """
    This function request data from API
    :param ticker: str
    :param duration: str
    :return: dict
    """
    data = requests.get(API_URL.format(ticker=ticker, duration=duration))
    if data.status_code == 404:
        return
    return data.json()


def get_prices(ticker):
    """
    Get prices for ticker
    :param ticker: str
    :return: list
    """
    data = request_data(ticker)
    prices = []
    if data:
        for d in data:
            prices += [v for k, v in d.items() if k in ['open', 'high', 'low', 'close']]
        return prices

