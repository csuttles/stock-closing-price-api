import os
import requests

from cachetools import cached, TTLCache
from flask_restful import Resource
from requests import HTTPError
from statistics import mean


class StockPrice(Resource):

    def get(self):
        '''
        This is the function called when clients hit the route.
        A StockData object is instantiated and used to return the results to the client
        If the data source ever changes (like a local DB instead), this can be used to pass additional params as needed
        :return: dict
        '''
        sd = StockData()
        return sd.get()


class StockData(object):
    """
    This class handles retrieving stock data from an upstream API
    Over time, it can be changes or extended.
    It's an abstraction layer so that we can change the source of our stock data without changing the interface.
    """

    def __init__(self):
        '''

        '''
        self.symbol = os.getenv("SYMBOL") or "MSFT"
        self.NDAYS = int(os.getenv("NDAYS") or "5")
        #  curl 'https://www.alphavantage.co/query?apikey=C227WD9W3LUVKVV9&function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT'
        self.url = 'https://www.alphavantage.co/query?'
        self.api_key = os.getenv("APIKEY") or "C227WD9W3LUVKVV9"
        self.api_function = "TIME_SERIES_DAILY_ADJUSTED"
        self.params = {
            "apikey": self.api_key,
            "function": self.api_function,
            "symbol": self.symbol,
        }

    # cache the data from our upstream API so we don't make excessive calls and exceed the APIKEY quota
    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def _get(self) -> dict:
        '''
        This defines the fetch of our upstream data and returns it
        :param url:
        :param params:
        :return:
        '''
        try:
            resp = requests.get(self.url, params=self.params)

            # If the response was successful, no Exception will be raised
            resp.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        return resp.json()

    def get(self)-> dict:
        '''
        Call this method to get the formatted stock data
        :return: stock data formatted according to the brief
        '''
        # get the data
        data = self._get()

        if not data:
            raise requests.HTTPError

        # trim the data to ndays
        # data has holes in it so use number of records instead of dates
        count = 0
        timeseries = dict()
        for calendar in data['Time Series (Daily)']:
            if count == self.NDAYS:
                break
            timeseries[calendar] = data['Time Series (Daily)'][calendar]
            count += 1

        # calculate closing average
        closing_avg = mean([float(timeseries[x]['4. close']) for x in timeseries])

        # assemble the return in json format consistent with upstream API
        # metadata, timeseries, and average closing price
        ret = dict()
        ret['meta'] = data['Meta Data']
        ret['timeseries'] = timeseries
        ret['closing_average'] = str("%.2f" % closing_avg)

        # return the result
        return ret

