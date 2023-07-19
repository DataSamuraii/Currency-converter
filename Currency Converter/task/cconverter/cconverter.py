import requests

currency_dict = {}

message_dict = {
    'base_currency': 'Please enter the base currency: ',
    'target_currency': 'Please enter the target currency: ',
    'amount': 'Please enter the amount: ',
    'checking_cache': 'Checking the cache...',
    'not_in_cache': 'Sorry, but it is not in the cache!',
    'in_cache': 'Oh! It is in the cache!',
    'error_api': 'There was an error contacting the Exchange Rate API',
    'not_understand': 'Sorry, I did not understand that.',
}


def get_exchange_rate(base_currency, target_currency):
    print(message_dict['checking_cache'])
    if target_currency not in currency_dict:
        print(message_dict['not_in_cache'])
        try:
            r = requests.get(f'https://www.floatrates.com/daily/{base_currency}.json').json()
            rate = r.get(target_currency, {}).get('rate')
            if rate:
                currency_dict[target_currency] = rate
            else:
                print(f"Could not get rate for {target_currency}")
                return None
        except requests.RequestException:
            print(message_dict['error_api'])
            return None
    else:
        print(message_dict['in_cache'])
    return currency_dict[target_currency]


def calculate_changed_amount(amount, rate):
    return round(amount * rate, 2)


def get_input(message, type_=None, min_=None, max_=None):
    while True:
        user_input = input(message)
        if type_ is not None:
            try:
                user_input = type_(user_input)
            except ValueError:
                print(message_dict['not_understand'])
                continue
        if min_ is not None and user_input < min_:
            print(f'Sorry, the value cannot be less than {min_}.')
        elif max_ is not None and user_input > max_:
            print(f'Sorry, the value cannot be more than {max_}.')
        else:
            return user_input


def main():
    base_currency = get_input(message_dict['base_currency'], type_=str).lower()
    target_currency = get_input(message_dict['target_currency'], type_=str).lower()
    amount = get_input(message_dict['amount'], type_=int)

    while True:
        rate = get_exchange_rate(base_currency, target_currency)
        if rate is None:
            break
        converted_amount = calculate_changed_amount(amount, rate)
        print(f'You received {converted_amount} {target_currency.upper()}')

        target_currency = get_input(message_dict['target_currency'], type_=str).lower()
        if not target_currency:
            break
        amount = get_input(message_dict['amount'], type_=int)


if __name__ == "__main__":
    main()
