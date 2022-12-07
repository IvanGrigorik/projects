import requests
from bs4 import BeautifulSoup


def grub_exchange_rate() -> dict:
    source = requests.get('https://myfin.by/bank/kursy_valjut_nbrb').text
    soup = BeautifulSoup(source, 'lxml')
    exchange_rate_table = soup.find('table', class_='default-table').find('tbody').find_all('tr')
    rate_from_BY = dict()
    rate_from_BY['BYN'] = 1

    for i in range(3):
        line = exchange_rate_table[i]
        rate_from_BY[line.next.next_sibling.next_sibling.text] \
            = float(line.next.next_sibling.text) / float(
            line.next.next_sibling.next_sibling.next_sibling.next_sibling.next)
    return rate_from_BY


def grub_currencies_rate() -> (list, list, list, list, list):
    """Return tuple of lists, which contain next strings: bank names, USD rate, EUR rate, RUB100 rate, EUR_USD rate"""
    source = requests.get('https://myfin.by/currency/minsk').text
    soup = BeautifulSoup(source, 'lxml')
    table = soup.find('tbody', class_='sort_body')

    banks = table.find_all('tr')
    banks_info = dict()
    USD_list = list()
    EUR_list = list()
    RUB100_list = list()
    EUR_USD_list = list()
    currencies = [USD_list, EUR_list, RUB100_list, EUR_USD_list]

    for bank in banks:
        try:
            bank_rate = list()
            name = ''

            # Collect all information about bank
            for bank_info in bank:
                # ! DO NOT Rewrite to regEx (Extremely slow!!)
                # If bank doesn't sell currencies
                if str(bank_info) == '<td class="currencies-courses__currency-cell ' \
                                     'currencies-courses__currency-cell--empty">-</td>':
                    bank_rate.append(None)

                # Bank name
                elif bank_info.find('img'):
                    # if bank_info.span.img is not None:
                    name = str(bank_info.span.img).split('\"')[1]

                # Bank currency
                else:
                    bank_rate.append(float(bank_info.span.text))

            banks_info[name] = bank_rate

        except Exception as e:
            # Exceptions with NoneType objects (collect only bank currencies)
            continue

    bank_names = list()
    for bank_name in banks_info.keys():
        bank_names.append(bank_name)

    # Parse data
    number_dict = {'USD': 0, 'EUR': 2, 'RUB_100': 4, 'EUR_USD': 5}
    for x, currency in enumerate(number_dict.values()):
        for bank in banks_info:
            currencies[x].append((banks_info[bank][currency], banks_info[bank][currency + 1]))

    return bank_names, USD_list, EUR_list, RUB100_list, EUR_USD_list
