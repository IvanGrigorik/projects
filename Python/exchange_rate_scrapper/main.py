# Created by SiFi
# Simple scrapper, that uses currency rate and output it in text format
# Created without commercial purpose
import tkinter
from functools import partial
from grubber import *

from customtkinter import *

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
        self.geometry("1440x990")
        # TODO: make resizable app
        self.resizable(False, False)

        self.title("MoneyWatch")

        self.__waiting_text = CTkTextbox(self)
        self.waiting_text()
        # Wait till request end
        self.__currencies = CurrencyParser()
        self.__waiting_text.destroy()

        self.update()

        # Bank names left bar

        # Top bar variables
        self.__currencies_top_bar_buttons = None
        self.__currencies_names_frame = CTkFrame(self)
        self.__buy_sell_buttons = None
        self.draw_top_bar()

        self.__banks_button_frame = CTkFrame(self)
        self.__bank_button = CTkButton(self)
        self.draw_bank_button()

        self.__banks_info_frame = None
        self.__bank_names_text = None
        self.draw_bank_names()

        self.__curr_rate_text = None
        self.draw_currencies_rate()
        print("Ready to use!")

    def waiting_text(self):
        self.__waiting_text = CTkTextbox(master=self,
                                         fg_color='#1A1A1A',
                                         activate_scrollbars=False)
        self.__waiting_text.tag_config("centralize_text", justify="center")
        self.__waiting_text.insert("1.0", "Waiting...", "centralize_text")
        self.__waiting_text.configure(state="disable")  # Only read
        self.__waiting_text.pack(padx=0, pady=self.winfo_height() / 3)
        self.update()

    def sort_currencies_callback(self, sort_value: str):
        self.__currencies.banks_info.sort(key=lambda x, y: x.USD.buy < y.USD.buy)
        # self.banks_info.sort(key=lambda x: x.name)  # Sorted by bank name
        # self.draw_bank_names()
        # self.draw_currencies_rate()
        print(f"Hello, {sort_value}")
        self.update()
        pass

    def draw_top_bar(self):
        # Draw top bar text (USD, EUR, RUB100, EUR_USD)
        self.__currencies_names_frame = CTkFrame(master=self,
                                                 corner_radius=8,
                                                 height=50, width=self.winfo_width() - 20)
        self.__currencies_names_frame.grid(row=0, column=1, pady=10, sticky=N)

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
            new_buy_sell_button("Buy", currency)
            self.__buy_sell_buttons[-1].grid(row=1, column=column_num, pady=10)
            new_buy_sell_button("Sell", currency)
            self.__buy_sell_buttons[-1].grid(row=1, column=column_num + 1, pady=10)
            column_num += 2

        self.update()

    def draw_bank_button(self):
        self.__banks_button_frame = CTkFrame(master=self,
                                             corner_radius=8,
                                             height=97,
                                             width=int(self.winfo_width() / 4))
        self.__banks_button_frame.grid_propagate(False)  # Set static-size frame
        self.__banks_button_frame.grid_columnconfigure(0, weight=1)  # Centralize all widgets inside
        self.__banks_button_frame.grid_rowconfigure(0, weight=1)  # Centralize all widgets inside

        self.__banks_button_frame.grid(row=0, column=0, padx=10, pady=10)

        self.update()  # To get __banks_button_frame width

        self.__bank_button = CTkButton(master=self.__banks_button_frame, text="Bank names",
                                       width=self.__banks_button_frame.winfo_width() - 20,
                                       height=50,
                                       corner_radius=4, command=partial(self.sort_currencies_callback, "banks"))
        self.__bank_button.grid()

        self.update()

    def draw_bank_names(self):
        # Draw only bank names (as a text)
        self.__banks_info_frame = CTkFrame(master=self,
                                           corner_radius=8,
                                           height=self.winfo_height() -
                                                  self.__banks_button_frame.winfo_height() - 30,
                                           width=self.__banks_button_frame.winfo_width() +
                                                 self.__currencies_names_frame.winfo_width() + 20)
        self.__banks_info_frame.grid_propagate(False)  # Set static-size frame

        # self.__banks_info.grid_columnconfigure(0, weight=1)  # Centralize all widgets inside
        self.__banks_info_frame.grid(row=1, column=0, columnspan=3, padx=15, pady=0, sticky=W)

        self.__bank_names_text = list()
        for pos, bank in enumerate(self.__currencies.banks_info):
            self.__bank_names_text.append(CTkTextbox(master=self.__banks_info_frame,
                                                     height=5, width=self.__bank_button.winfo_width(),
                                                     activate_scrollbars=False))
            self.__bank_names_text[-1].insert(f"0.0", bank.name)
            self.__bank_names_text[-1].configure(state="disable")
            self.__bank_names_text[-1].grid(row=pos + 1, column=0, padx=20, pady=5)

        self.update()

    def add_rate_text(self, rate, t_row, t_column):
        if rate is None:
            rate = '-'
        self.__curr_rate_text.append(CTkTextbox(master=self.__banks_info_frame,
                                                height=5,
                                                width=self.__buy_sell_buttons[-1].winfo_width(),
                                                activate_scrollbars=False))
        self.__curr_rate_text[-1].insert(f"0.0", rate)
        self.__curr_rate_text[-1].configure(state="disable")
        self.__curr_rate_text[-1].grid(row=t_row, column=t_column, padx=10, pady=5)

    def draw_currencies_rate(self):
        self.__curr_rate_text = list()

        for row, bank in enumerate(self.__currencies.banks_info):
            column = 3
            for field in fields(bank):
                if field.name != "name":
                    self.add_rate_text(getattr(getattr(bank, field.name), "buy"), row + 1, column)
                    self.add_rate_text(getattr(getattr(bank, field.name), "sell"), row + 1, column + 1)
                    column += 2
        pass


# def draw_bank_currencies(self):


if __name__ == "__main__":
    app = App()

    app.mainloop()
    pass
