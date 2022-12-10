# Created by SiFi
# Simple scrapper, that uses currency rate and output it in text format
# Created without commercial purpose
from grubber import *

from customtkinter import *
import tkinter

from functools import partial

set_appearance_mode("dark")
set_default_color_theme("dark-blue")


class CurrencyParser:
    currencies_names = ["USD", "EUR", "RUB100", "EUR_USD"]

    def __init__(self):
        # TODO: uncomment
        self.__exchange_rate_table = grub_exchange_rate()
        self.banks_info = grub_currencies_rate()
        self.banks_info.sort(key=lambda x: x.name)  # Sorted by bank name
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


class App(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("1440x980")
        # TODO: make resizable app
        self.resizable(False, False)

        self.title("MoneyWatch")

        self.__waiting_text = CTkTextbox(self)
        self.waiting_text()
        # Wait till request end
        self.__currencies = CurrencyParser()
        self.__waiting_text.destroy()

        self.update()


        # Main tab with currencies rates
        self.__currencies_top_bar_buttons = None
        self.__currencies_names_frame = CTkFrame(self)
        self.__buy_sell_buttons = None

        self.__banks_button_frame = CTkFrame(self)
        self.__bank_button = CTkButton(self)
        self.__banks_info_frame = None
        self.__curr_rate_text = None
        self.__bank_names_text = None
        self.__tabview = None
        self.draw_tabs()

        self.update()

        print("Ready to use!")

    def draw_tabs(self):
        self.draw_tabview()
        self.draw_curr_rates()

    def draw_tabview(self):
        self.__tabview = CTkTabview(self, width=1000)
        self.__tabview.add("Currencies")
        self.__tabview.add("Converter")
        self.__tabview.add("Charts")
        self.__tabview.set("Currencies")
        self.__tabview.pack(padx=0, pady=0)
        pass

    def draw_curr_rates(self):
        # Top bar variables (USD/EUR/RUB100/EUR_RUB, buy/sell buttons)
        self.draw_top_bar()

        # Button which sorted by bank names
        self.draw_bank_button()

        # Main frame with bank names and currencies
        self.define_bank_names_position()
        self.draw_currencies_rate()

    def waiting_text(self):
        self.__waiting_text = CTkTextbox(master=self,
                                         fg_color='#1A1A1A',
                                         activate_scrollbars=False)
        self.__waiting_text.tag_config("centralize_text", justify="center")
        self.__waiting_text.insert("1.0", "Waiting...", "centralize_text")
        self.__waiting_text.configure(state="disable")  # Only read
        self.__waiting_text.pack(padx=0, pady=self.winfo_height() / 3)
        self.update()

    def operation(self, curr, b_or_s):
        # IDK how do it easier for current architecture
        match curr:
            case "USD":
                self.__currencies.banks_info.sort(key=lambda x: x.USD.buy) if b_or_s == "buy" else \
                    self.__currencies.banks_info.sort(key=lambda x: x.USD.sell, reverse=True)

            case "EUR":
                self.__currencies.banks_info.sort(key=lambda x: x.EUR.buy) if b_or_s == "buy" else \
                    self.__currencies.banks_info.sort(key=lambda x: x.EUR.sell, reverse=True)

            case "RUB100":
                self.__currencies.banks_info.sort(key=lambda x: x.RUB100.buy) if b_or_s == "buy" else \
                    self.__currencies.banks_info.sort(key=lambda x: x.RUB100.sell, reverse=True)

            case "EUR_USD":
                self.__currencies.banks_info.sort(key=lambda x: x.EUR_USD.buy) if b_or_s == "buy" else \
                    self.__currencies.banks_info.sort(key=lambda x: x.EUR_USD.sell, reverse=True)

    def sort_currencies_callback(self, sort_value: str):
        if sort_value == "banks":
            self.__currencies.banks_info.sort(key=lambda x: x.name)  # Sorted by bank name
        else:
            b_or_s, curr = sort_value.split(" ")
            self.operation(curr, b_or_s)
        self.set_banks_text()
        self.set_rate_text()

    def draw_top_bar(self):
        # Draw top bar text (USD, EUR, RUB100, EUR_USD)
        self.__currencies_names_frame = CTkFrame(master=self.__tabview.tab("Currencies"),
                                                 corner_radius=8,
                                                 height=50, width=1420)
        # self.__currencies_names_frame
        self.__currencies_names_frame.grid(row=0, column=1, pady=10, padx=0, sticky=N)

        self.__currencies_top_bar_buttons = list()
        column_num = 0
        for currency_name in self.__currencies.currencies_names:
            self.__currencies_top_bar_buttons.append(CTkTextbox(master=self.__currencies_names_frame,
                                                                width=200, height=20,
                                                                activate_scrollbars=False))
            self.__currencies_top_bar_buttons[-1].tag_config("centralize_text", justify="center")
            self.__currencies_top_bar_buttons[-1].insert(f"0.0", currency_name, "centralize_text")
            self.__currencies_top_bar_buttons[-1].configure(state="disable")

            self.__currencies_top_bar_buttons[-1].grid(row=0, column=column_num, columnspan=2, padx=10, pady=10)
            column_num += 2

        # Draw buy/sell buttons
        self.__buy_sell_buttons = list()
        column_num = 0
        new_buy_sell_button = lambda b_or_s, curr: self.__buy_sell_buttons.append(
            CTkButton(master=self.__currencies_names_frame,
                      width=90, height=20, corner_radius=4,
                      text=b_or_s,
                      command=partial(self.sort_currencies_callback, f"{b_or_s} {curr}")))

        for currency in self.__currencies.currencies_names:
            new_buy_sell_button("buy", currency)
            self.__buy_sell_buttons[-1].grid(row=1, column=column_num, pady=10)
            new_buy_sell_button("sell", currency)
            self.__buy_sell_buttons[-1].grid(row=1, column=column_num + 1, pady=10)
            column_num += 2

        # self.update()

    def draw_bank_button(self):
        self.__banks_button_frame = CTkFrame(master=self.__tabview.tab("Currencies"),
                                             corner_radius=8,
                                             height=97,
                                             width=360)
        self.__banks_button_frame.grid_propagate(False)  # Set static-size frame
        self.__banks_button_frame.grid_columnconfigure(0, weight=1)  # Centralize all widgets inside
        self.__banks_button_frame.grid_rowconfigure(0, weight=1)  # Centralize all widgets inside

        self.__banks_button_frame.grid(row=0, column=0, padx=10, pady=10)

        self.update()  # To get __banks_button_frame width

        self.__bank_button = CTkButton(master=self.__banks_button_frame, text="Bank names",
                                       width=340,
                                       height=50,
                                       corner_radius=4, command=partial(self.sort_currencies_callback, "banks"))
        self.__bank_button.grid()

    def set_banks_text(self):
        for i, bank in enumerate(self.__currencies.banks_info):
            self.__bank_names_text[i].configure(text=bank.name)

    def define_bank_names_position(self):
        # Draw only bank names (as a text)
        self.__banks_info_frame = CTkFrame(master=self.__tabview.tab("Currencies"), corner_radius=8,
                                           height=840, width=1260)
        self.__banks_info_frame.grid_propagate(False)  # Set static-size frame
        self.__banks_info_frame.grid(row=1, column=0, columnspan=3, padx=15, pady=0, sticky=W)

        self.__bank_names_text = list()
        for pos, bank in enumerate(self.__currencies.banks_info):
            self.__bank_names_text.append(CTkLabel(master=self.__banks_info_frame,
                                                   height=30, width=340,
                                                   fg_color=("#1A1A1A", "#333333"),
                                                   corner_radius=4))
            self.__bank_names_text[-1].grid_propagate(False)
            self.__bank_names_text[-1].grid(row=pos + 1, column=0, padx=20, pady=5)
        self.set_banks_text()

    def set_rate_text(self):
        rate_num = 0
        for i, bank in enumerate(self.__currencies.banks_info):
            for field in fields(bank):
                if field.name != "name":
                    rate_buy = getattr(getattr(bank, field.name), "buy")
                    rate_sell = getattr(getattr(bank, field.name), "sell")
                    if not rate_buy or not rate_buy:
                        rate_sell = '-'
                        rate_buy = '-'
                    self.__curr_rate_text[rate_num].configure(text=rate_buy)
                    self.__curr_rate_text[rate_num + 1].configure(text=rate_sell)
                    rate_num += 2

    def define_rates_position(self, t_row, t_column):
        self.__curr_rate_text.append(CTkLabel(master=self.__banks_info_frame,
                                              height=30, width=90,
                                              fg_color=("#1A1A1A", "#333333"),
                                              corner_radius=4))
        self.__curr_rate_text[-1].grid_propagate(False)
        self.__curr_rate_text[-1].grid(row=t_row, column=t_column, padx=10, pady=5)

    def draw_currencies_rate(self):
        self.__curr_rate_text = list()

        for row, bank in enumerate(self.__currencies.banks_info):
            column = 3
            for field in fields(bank):
                if field.name != "name":
                    self.define_rates_position(row + 1, column)
                    self.define_rates_position(row + 1, column + 1)
                    column += 2
        self.set_rate_text()
        pass


if __name__ == "__main__":
    app = App()

    app.mainloop()
    pass
