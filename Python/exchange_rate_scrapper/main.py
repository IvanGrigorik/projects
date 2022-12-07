# Created by SiFi
# Simple scrapper, that uses currency rate and output it in text format
# Created without commercial purpose
import tkinter
from functools import partial
from grubber import *

import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


def sort_currencies(sort_value: str):
    print(f"Hello, {sort_value}")
    pass


class CurrencyParser:
    currencies_names = ["USD", "EUR", "RUB100", "EUR_USD"]

    def __init__(self):
        # TODO: uncomment
        self.__exchange_rate_table = grub_exchange_rate()
        self.bank_names, self.USD_list, \
            self.EUR_list, self.RUB100_list, self.EUR_USD_list = grub_currencies_rate()
        self.currencies_lists = [self.USD_list, self.EUR_list, self.RUB100_list, self.EUR_USD_list]
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

        self.__waiting_text = customtkinter.CTkTextbox(self)
        self.waiting_text()
        # Wait till request end
        self.__currencies = CurrencyParser()
        self.__waiting_text.destroy()

        self.update()

        # Bank names left bar

        # Top bar variables
        self.__currencies_top_bar = None
        self.__currencies_names_frame = customtkinter.CTkFrame(self)
        self.__buy_sell_buttons = None
        self.draw_top_bar()

        self.__banks_button_frame = customtkinter.CTkFrame(self)
        self.__bank_button = None
        self.draw_bank_button()

        self.__banks_info = None
        self.__bank_names_text = None
        self.draw_banks_info()

    def waiting_text(self):
        self.__waiting_text = customtkinter.CTkTextbox(master=self,
                                                       fg_color='#1A1A1A',
                                                       activate_scrollbars=False)
        self.__waiting_text.tag_config("centralize_text", justify="center")
        self.__waiting_text.insert("1.0", "Waiting...", "centralize_text")
        self.__waiting_text.configure(state="disable")  # Only read
        self.__waiting_text.pack(padx=0, pady=self.winfo_height() / 3)
        self.update()

    def draw_top_bar(self):
        # Draw top bar text (USD, EUR, RUB100, EUR_USD)
        self.__currencies_names_frame = customtkinter.CTkFrame(master=self,
                                                               corner_radius=8,
                                                               height=50, width=self.winfo_width() - 20)
        self.__currencies_names_frame.grid(row=0, column=1, pady=10, sticky=customtkinter.N)

        self.__currencies_top_bar = list()
        column_num = 0
        for currency_name in self.__currencies.currencies_names:
            self.__currencies_top_bar.append(customtkinter.CTkTextbox(master=self.__currencies_names_frame,
                                                                      width=200, height=20,
                                                                      activate_scrollbars=False))
            self.__currencies_top_bar[-1].tag_config("centralize_text", justify="center")
            self.__currencies_top_bar[-1].insert(f"0.0", currency_name, "centralize_text")
            self.__currencies_top_bar[-1].configure(state="disable")

            self.__currencies_top_bar[-1].grid(row=0, column=column_num, columnspan=2, padx=10, pady=10)
            column_num += 2

        # Draw buy/sell buttons
        self.__buy_sell_buttons = list()
        column_num = 0
        new_buy_sell_button = lambda b_or_s, curr: \
            self.__buy_sell_buttons.append(customtkinter.
                                           CTkButton(master=self.__currencies_names_frame,
                                                     width=90, height=20, corner_radius=4,
                                                     text=b_or_s,
                                                     command=partial(sort_currencies, f"{b_or_s}_{curr}")))
        for currency in self.__currencies.currencies_names:
            new_buy_sell_button("Buy", currency)
            self.__buy_sell_buttons[-1].grid(row=1, column=column_num, pady=10)
            new_buy_sell_button("Sell", currency)
            self.__buy_sell_buttons[-1].grid(row=1, column=column_num + 1, pady=10)
            column_num += 2

        self.update()

    def draw_bank_button(self):
        self.__banks_button_frame = customtkinter.CTkFrame(master=self,
                                                           corner_radius=8,
                                                           height=97,
                                                           width=int(self.winfo_width() / 4))
        self.__banks_button_frame.grid_propagate(False)  # Set static-size frame
        self.__banks_button_frame.grid_columnconfigure(0, weight=1)  # Centralize all widgets inside
        self.__banks_button_frame.grid_rowconfigure(0, weight=1)  # Centralize all widgets inside

        self.__banks_button_frame.grid(row=0, column=0, padx=10, pady=10)

        self.update()  # To get __banks_button_frame width

        self.__bank_button = customtkinter.CTkButton(master=self.__banks_button_frame, text="Bank names",
                                                     width=self.__banks_button_frame.winfo_width() - 20,
                                                     height=50,
                                                     corner_radius=4, command=partial(sort_currencies, "banks"))
        self.__bank_button.grid()

        self.update()

    def draw_banks_info(self):
        # Draw only bank names (as a text)
        self.__banks_info = customtkinter.CTkFrame(master=self,
                                                   corner_radius=8,
                                                   height=self.winfo_height() -
                                                          self.__banks_button_frame.winfo_height() - 20,
                                                   width=self.__banks_button_frame.winfo_width() +
                                                         self.__currencies_names_frame.winfo_width() + 20)
        self.__banks_info.grid_propagate(False)  # Set static-size frame

        # self.__banks_info.grid_columnconfigure(0, weight=1)  # Centralize all widgets inside
        self.__banks_info.grid(row=1, column=0, columnspan=3, padx=15, pady=0, sticky=customtkinter.W)

        self.__bank_names_text = list()
        for pos, name in enumerate(self.__currencies.bank_names):
            self.__bank_names_text.append(customtkinter.CTkTextbox(master=self.__banks_info,
                                                                   height=5,
                                                                   activate_scrollbars=True), )
            self.__bank_names_text[-1].insert(f"0.0", name)
            self.__bank_names_text[-1].configure(state="disable")
            self.__bank_names_text[-1].grid(row=pos + 1, column=0, padx=5, pady=5)

        self.update()


if __name__ == "__main__":
    app = App()

    app.mainloop()
    pass
