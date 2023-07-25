import requests

currency_dict = {}

sys_message_dict = {
    'input_base_currency': 'Please enter the base currency: ',
    'input_target_currency': 'Please enter the target currency: ',
    'input_amount': 'Please enter the amount: ',
    'cache_check': 'Checking the cache...',
    'cache_miss': 'Sorry, but it is not in the cache!',
    'cache_hit': 'Oh! It is in the cache!',
    'api_error': 'There was an error contacting the Exchange Rate API',
    'rate_error': 'Sorry, couldn\'t retrieve exchange rate.',
    'invalid_input': 'Sorry, I did not understand that.',
    'invalid_option': 'Invalid option, please choose a valid option.',
    'conversion_conf': 'Please set the base currency, target currency, and amount first.',
    'exit': 'Exiting ATM. Good bye!'
}


def get_json(base_currency):
    r = requests.get(f'https://www.floatrates.com/daily/{base_currency}.json').json()
    if not r:
        print(f'Invalid currency: {base_currency}')
        return None
    return r


def get_exchange_rate(base_currency, target_currency):
    print(sys_message_dict['cache_check'])
    if target_currency not in currency_dict:
        print(sys_message_dict['cache_miss'])
        try:
            r = get_json(base_currency)
            rate = r.get(target_currency, {}).get('rate')
            if rate:
                currency_dict[target_currency] = rate
            else:
                print(f"Could not get rate for {target_currency}")
                return None
        except requests.RequestException:
            print(sys_message_dict['api_error'])
            return None
    else:
        print(sys_message_dict['cache_hit'])
    return currency_dict[target_currency]


def calculate_changed_amount(amount, rate):
    return round(amount * rate, 2)


def get_currency(message):
    user_input = input(message).lower()
    return user_input


def get_amount(message, min_=None, max_=None):
    while True:
        user_input = input(message)
        try:
            user_input = int(user_input)
        except ValueError:
            print(sys_message_dict['invalid_input'])
            continue
        if min_ is not None and user_input < min_:
            print(f'Sorry, the value cannot be less than {min_}.')
        elif max_ is not None and user_input > max_:
            print(f'Sorry, the value cannot be more than {max_}.')
        else:
            return user_input


def get_ui():
    ui_message_dict = {
        'select_opt': '\nPlease select an option:',
        'set_base_currency': '1: Set base currency',
        'set_target_currency': '2: Set target currency',
        'set_amount': '3: Set amount',
        'convert': '4: Convert amount',
        'exit': '5. Exit'
    }

    for x in ui_message_dict:
        print(ui_message_dict[x])


def main():
    base_currency = None
    target_currency = None
    amount = None

    while True:
        get_ui()
        option = input("> ")

        if option == '1':
            base_currency = get_currency(sys_message_dict['input_base_currency'])
        elif option == '2':
            target_currency = get_currency(sys_message_dict['input_target_currency'])
        elif option == '3':
            amount = get_amount(sys_message_dict['input_amount'])
        elif option == '4':
            if base_currency and target_currency and amount:
                rate = get_exchange_rate(base_currency, target_currency)
                if rate is None:
                    print(sys_message_dict['rate_error'])
                    continue
                converted_amount = calculate_changed_amount(amount, rate)
                print(f'You received {converted_amount} {target_currency.upper()}')
            else:
                print(sys_message_dict['conversion_conf'])
        elif option == '5':
            print(sys_message_dict['exit'])
            break
        else:
            print(sys_message_dict['invalid_option'])
            get_ui()


if __name__ == "__main__":
    main()
