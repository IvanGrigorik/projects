# Created by SiFi
# Simple scrapper, that uses currency rate and output it in text format
# Created without commercial purpose


import customtkinter
from grubber import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class CurrencyParser:
    # Private members
    def __init__(self):
        self.__exchange_rate_table = grub_exchange_rate()
        self.refresh_rate()
        self.bank_names, self.USD_list, \
            self.EUR_list, self.RUB100_list, self.EUR_USD_list = grub_currencies_rate()

    def refresh_rate(self):
        self.__exchange_rate_table = grub_exchange_rate()

    def currency_nbrb(self, source_currency: str, destination_currency: str, amount: float) -> float:
        if source_currency in self.__exchange_rate_table.keys() and \
                destination_currency in self.__exchange_rate_table.keys():
            return amount * self.__exchange_rate_table[source_currency] / \
                self.__exchange_rate_table[destination_currency]
        else:
            raise Exception("Mismatch currency")


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("1280x720")
        self.title("MoneyWatch")

        self.__main_frame = customtkinter.CTkFrame(master=self, corner_radius=8)
        self.__main_frame.pack()



if __name__ == "__main__":
    app = App()
    currencies = CurrencyParser()

    app.mainloop()
    pass
