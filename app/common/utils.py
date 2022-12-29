import os

NDAYS = os.getenv("NDAYS")


def ndays(data, ndays=NDAYS) -> dict:
    """
    takes a json dict, and number of days, trims data to ndays
    :param data: dict of stock data
    :param ndays: number of days.
    :return: dict of only ndays data
    """
    pass

