# Created by SiFi
# Simple scrapper, that uses currency rate and output it in text format
# Created without commercial purpose
import tkinter

import customtkinter
from grubber import *
from functools import partial

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


def sort_currencies(sort_value: str):
    print(f"Hello, {sort_value}")
    pass


class CurrencyParser:
    currencies_names = ["USD", "EUR", "RUB100", "EUR_USD"]

    def __init__(self):
        # TODO: uncomment
        # self.__exchange_rate_table = grub_exchange_rate()
        # self.bank_names, self.USD_list, \
        #     self.EUR_list, self.RUB100_list, self.EUR_USD_list = grub_currencies_rate()
        pass

    def refresh_rate(self):
        # TODO: uncomment
        # self.__exchange_rate_table = grub_exchange_rate()
        # self.bank_names, self.USD_list, \
        #     self.EUR_list, self.RUB100_list, self.EUR_USD_list = grub_currencies_rate()
        pass

    def convert_currency(self, source_currency: str, destination_currency: str, amount: float) -> float:
        """In: USD/EUR/RUB/BYN: str, USD/EUR/RUB/BYN: str, sum_to_convert: float"""
        # TODO: uncomment
        # if source_currency in self.__exchange_rate_table.keys() and \
        #         destination_currency in self.__exchange_rate_table.keys():
        #     return amount * self.__exchange_rate_table[source_currency] / \
        #         self.__exchange_rate_table[destination_currency]
        # else:
        #     raise Exception("Mismatch currency")


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("1440x960")
        # TODO: make resizable app
        self.resizable(False, False)

        self.title("MoneyWatch")
        self.update()
        self.__waiting_text = customtkinter.CTkTextbox(master=self,
                                                       fg_color='#1A1A1A',
                                                       activate_scrollbars=False)
        self.__waiting_text.tag_config("centralize_text", justify="center")
        self.__waiting_text.insert("1.0", "Waiting...", "centralize_text")
        self.__waiting_text.configure(state="disable")  # Only read
        self.__waiting_text.pack(padx=0, pady=self.winfo_height() / 3)
        self.update()

        self.__currencies = CurrencyParser()

        self.__waiting_text.destroy()
        self.update()

        # Bank names left bar
        self.__bank_names = customtkinter.CTkFrame(master=self,
                                                   corner_radius=8,
                                                   height=self.winfo_height() - 20,
                                                   width=int(self.winfo_width() / 4))
        self.__bank_names.grid_propagate(False)  # Set static-size frame
        self.__bank_names.grid_columnconfigure(0, weight=1)  # Centralize all widgets inside
        self.__bank_names.grid(row=0, column=0, padx=10, pady=10)
        self.update()  # To get __bank_names width
        self.__bank_button = customtkinter.CTkButton(master=self.__bank_names, text="Bank names",
                                                     width=self.__bank_names.winfo_width() - 20,
                                                     corner_radius=4, command=partial(sort_currencies, "banks"))
        self.__bank_button.grid(row=0, column=0, padx=10, pady=10)

        # Top bar (with currencies with the following names: USD, EUR, RUB100, EUR_USD)
        self.__currencies_names_frame = customtkinter.CTkFrame(master=self,
                                                               corner_radius=8,
                                                               height=50, width=self.winfo_width() - 20)
        self.__currencies_names_frame.grid(row=0, column=1, padx=0, pady=10, sticky=customtkinter.N)

        self.__currencies_top_bar = list()
        for x, currency_name in enumerate(self.__currencies.currencies_names):
            self.__currencies_top_bar.append(customtkinter.CTkTextbox(master=self.__currencies_names_frame,
                                                                      width=200, height=20, activate_scrollbars=False))
            self.__currencies_top_bar[x].tag_config("centralize_text", justify="center")
            self.__currencies_top_bar[x].insert(f"0.0", currency_name, "centralize_text")
            self.__currencies_top_bar[x].configure(state="disable")
            self.__currencies_top_bar[x].grid(row=0, column=x, padx=10, pady=10)

        self.update()

        pass


if __name__ == "__main__":
    app = App()

    app.mainloop()
    pass
