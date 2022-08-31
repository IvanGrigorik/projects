# Created by SiFi
# Simple scrapper, that uses currency rate and output it in text format
# Created without commercial purpose


from bs4 import BeautifulSoup
import requests

if __name__ == "__main__":
    source = requests.get('https://myfin.by/currency/minsk').text
    soup = BeautifulSoup(source, 'lxml')
    table = soup.find('tbody', class_='sort_body')

    banks = table.find_all('tr')
    # TODO: ReWrite without two lists.
    #  Use dictionary, that use bank name as key
    #  and exchange rate as value
    bank_names = list()
    currency_rates = list(list())

    for bank in banks:
        try:
            bank_rate = list()
            # Collect all information about bank
            for bank_info in bank:
                a = bank_info
                if str(bank_info) == '<td class="currencies-courses__currency-cell ' \
                                     'currencies-courses__currency-cell--empty">-</td>':
                    bank_rate.append(float(-1.0))
                    continue
                # Bank name
                if bank_info.span.img is not None:
                    name = str(bank_info.span.img).split('\"')[1]
                    bank_names.append(name)
                # Bank currency
                else:
                    curr = bank_info.text
                    bank_rate.append(float(bank_info.span.text))

            # Add currency rate into rates list
            currency_rates.append(bank_rate)

        except Exception as e:
            # Exceptions with NoneType objects (collect only bank names)
            continue

    for name, rate in zip(bank_names, currency_rates):
        print('{:<25}'.format(name), end='')
        for currency in rate:
            if currency < 0:
                print('{:<10}'.format('-'), end='')
                continue
            print('{:<10}'.format(currency), end='')
        print()
