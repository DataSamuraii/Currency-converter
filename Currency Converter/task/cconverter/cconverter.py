import requests
import re
from colorama import Fore, Style


class CurrencyConverter:
    SYS_MESSAGE_DICT = {
        'input_base_currency': 'Please enter the base currency (or multiple): ',
        'input_target_currency': 'Please enter the target currency (or multiple): ',
        'input_amount': 'Please enter the amount: ',
        'cache_check': 'Checking the cache...',
        'cache_miss': 'Sorry, but it is not in the cache!',
        'cache_hit': 'Oh! It is in the cache!',
        'api_error': 'There was an error contacting the Exchange Rate API',
        'rate_error': 'Sorry, couldn\'t retrieve exchange rate.',
        'less_than': 'Sorry, the value cannot be less than {}.',
        'more_than': 'Sorry, the value cannot be more than {}.',
        'invalid_input': 'Sorry, I did not understand that.',
        'invalid_option': 'Invalid option, please choose a valid option.',
        'conversion_conf': 'Please set the base currency, target currency, and amount first.',
        'exit': 'Exiting ATM. Good bye!'
    }

    def __init__(self):
        self.currency_dict = {}
        self.base_currency = None
        self.target_currency = None
        self.amount = None

    @staticmethod
    def get_json(base_currency):
        try:
            r = requests.get(f'https://www.floatrates.com/daily/{base_currency}.json')
            r.raise_for_status()
        except requests.RequestException as err:
            print(f"Error occurred: {err}")
            return None
        return r.json()

    def get_exchange_rate(self, base_currency, target_currency):
        print(self.SYS_MESSAGE_DICT['cache_check'])
        if target_currency not in self.currency_dict[base_currency]:
            print(self.SYS_MESSAGE_DICT['cache_miss'])
            r = self.get_json(base_currency)
            if r is None:
                print(self.SYS_MESSAGE_DICT['api_error'])
                return None
            rate = r.get(target_currency, {}).get('rate')
            if rate:
                self.currency_dict[base_currency][target_currency] = rate
            else:
                print(f"Could not get rate for {target_currency}")
                return None
        else:
            print(self.SYS_MESSAGE_DICT['cache_hit'])
        return self.currency_dict

    def get_currency(self, message, currency_type=None):
        print(Fore.CYAN + "Example: USD, EUR" + Style.RESET_ALL)
        user_input = input(Fore.GREEN + message + Style.RESET_ALL).lower()
        user_input = re.split(r',| ', user_input)
        if currency_type == 'base':
            for currency in user_input:
                if currency not in self.currency_dict:
                    self.currency_dict[currency] = {}
        return user_input

    def get_amount(self, message, min_=None, max_=None):
        while True:
            user_input = input(message)
            try:
                user_input = float(user_input)
            except ValueError:
                print(self.SYS_MESSAGE_DICT['invalid_input'])
                continue
            if min_ is not None and user_input < min_:
                print(self.SYS_MESSAGE_DICT['less_than'].format(min_))
            elif max_ is not None and user_input > max_:
                print(self.SYS_MESSAGE_DICT['more_than'].format(max_))
            else:
                return user_input

    @staticmethod
    def get_ui():
        print("\n" + "=" * 50)
        print("Currency Converter Menu:")
        print("=" * 50)
        print("1: Set base currency")
        print("2: Set target currency")
        print("3: Set amount")
        print("4: Convert amount")
        print("5: Exit")
        print("=" * 50)

    @staticmethod
    def calculate_changed_amount(amount, rate):
        return round(amount * rate, 2)

    def set_base_currency(self):
        self.base_currency = self.get_currency(self.SYS_MESSAGE_DICT['input_base_currency'], currency_type='base')

    def set_target_currency(self):
        self.target_currency = self.get_currency(self.SYS_MESSAGE_DICT['input_target_currency'])

    def set_amount(self):
        self.amount = self.get_amount(self.SYS_MESSAGE_DICT['input_amount'], min_=0)

    def convert_amount(self):
        if self.base_currency and self.target_currency and self.amount:
            for base_c in self.base_currency:
                for target_c in self.target_currency:
                    rate = self.get_exchange_rate(base_c, target_c)
                    if rate is None:
                        print(self.SYS_MESSAGE_DICT['rate_error'])
                        continue
                    converted_amount = self.calculate_changed_amount(self.amount, rate[base_c][target_c])
                    print(f'You received {converted_amount} {target_c.upper()}')
        else:
            print(self.SYS_MESSAGE_DICT['conversion_conf'])

    def exit_program(self):
        exit(self.SYS_MESSAGE_DICT['exit'])

    def run(self):
        print(Fore.YELLOW + "Welcome to Currency Converter!" + Style.RESET_ALL)
        print("Follow the prompts to convert currency.")
        while True:
            self.get_ui()
            option = input(Fore.GREEN + "> " + Style.RESET_ALL)

            options = {
                '1': self.set_base_currency,
                '2': self.set_target_currency,
                '3': self.set_amount,
                '4': self.convert_amount,
                '5': self.exit_program
            }

            if option in options:
                options[option]()
            else:
                print(self.SYS_MESSAGE_DICT['invalid_option'])
                self.get_ui()


if __name__ == "__main__":
    CurrencyConverter().run()
