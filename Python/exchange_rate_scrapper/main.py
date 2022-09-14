# Created by SiFi
# Simple scrapper, that uses currency rate and output it in text format
# Created without commercial purpose
import re

from bs4 import BeautifulSoup
import requests


# import re


# Find max element in dictionary lists index
# Example:
# example_dict = ('a': [1, 2, 3, 4],
#                 'b': [2, 3, 4, 5],
#                 'c': [3, 4, 5, 6])
# find_max(example_dict, 0) == 3
# find_max(example_dict, 3) == 6 and so on
def find_max(info: dict, index: int):
    max_value = 0
    for element in info:
        if info[element][index] > max_value:
            max_value = info[element][index]
    return max_value


def find_min(info: dict, index: int):
    max_value = 0
    for element in info:
        if info[element][index] < max_value:
            max_value = info[element][index]
    return max_value


if __name__ == "__main__":
    source = requests.get('https://myfin.by/currency/minsk').text
    soup = BeautifulSoup(source, 'lxml')
    table = soup.find('tbody', class_='sort_body')

    banks = table.find_all('tr')
    banks_info = dict()

    for bank in banks:
        try:
            bank_rate = list()
            name = ''
            # Collect all information about bank
            for bank_info in bank:
                a = bank_info

                # DO NOT! Rewrite to regEx (Extremely slow!!)
                if str(bank_info) == '<td class="currencies-courses__currency-cell ' \
                                     'currencies-courses__currency-cell--empty">-</td>':
                    bank_rate.append(float(-1.0))
                    continue
                # Bank name
                if bank_info.find('img'):
                    # if bank_info.span.img is not None:
                    name = str(bank_info.span.img).split('\"')[1]
                # Bank currency
                else:
                    bank_rate.append(float(bank_info.span.text))

            # TODO:
            banks_info[name] = bank_rate

        except Exception as e:
            # Exceptions with NoneType objects (collect only bank names)
            # count += 1
            # print(count)
            continue

    # Print additional info
    currencies = ['USD', 'EUR', 'RUB (100)', 'EUR/USD']
    print('{:<25}'.format('Bank'), end='')

    for currency in currencies:
        print(f'{currency}'.center(20), end='')
    print()
    print('{:<25}'.format(''), end='')
    buy_sell = ['Buy', 'Sell']
    for currency in currencies:
        for trade in buy_sell:
            print('{:<10}'.format(trade), end='')
    print()

    # Print currencies rate
    for bank in banks_info:
        print('{:<25}'.format(bank), end='')
        for currency in banks_info[bank]:
            if currency < 0:
                print('{:<10}'.format('-'), end='')
                continue
            print('{:<10}'.format(currency), end='')
        print()
