This is the *Currency Converter* project I made myself.


<p>Want to convert one currency to another? You can go to your bank website and do the math by yourself. Or you can write a program to do it quickly and efficiently! The Currency Converter is a simple console program that calculates the amount of money you get by converting one currency to another.</p>

# Currency Converter

## Overview

The Currency Converter is a console-based application that allows users to convert between different currencies. The conversion rates are fetched from a public API, and the application supports converting multiple base and target currencies at the same time.

## Installation

No special installation is required. You will need Python and the `requests` library. You can install the required library using pip:

```bash
pip install requests
```

## Usage

To run the Currency Converter, simply execute the script:

```bash
python currency_converter.py
```

### Main Menu

Upon running the application, you'll be presented with the main menu, allowing you to perform the following actions:

1. **Set Base Currency**: Input one or more base currencies, separated by commas or spaces.
2. **Set Target Currency**: Input one or more target currencies, separated by commas or spaces.
3. **Set Amount**: Input the amount to be converted.
4. **Convert Amount**: Perform the conversion based on the previously entered base currencies, target currencies, and amount.
5. **Exit**: Exit the application.

### Cache System

The application includes a caching system that stores previously retrieved exchange rates. If a rate is already in the cache, it will be used instead of fetching from the API.

## Classes and Methods

### `CurrencyConverter`

This class encapsulates the logic for currency conversion.

#### Methods

- `get_json(base_currency)`: Fetches exchange rates for a given base currency.
- `get_exchange_rate(base_currency, target_currency)`: Retrieves the exchange rate between two currencies.
- `calculate_changed_amount(amount, rate)`: Calculates the converted amount based on the given rate.
- `get_currency(message, currency_type=None)`: Gets user input for currencies.
- `get_amount(message, min_=None, max_=None)`: Gets user input for an amount, with optional min and max validation.
- `get_ui()`: Displays the user interface for selecting options.
- `run()`: Main loop to run the currency converter application.

## Limitations

1. The application does not perform thorough validation on currency codes, so user input must be valid according to the API.
2. The caching system does not have a built-in expiration, so cached rates may become stale.
3. There's no built-in support for handling all possible API errors or exceptions.

## License

The code is provided as-is without any warranty. You are free to modify, distribute, or use it as you see fit.

## Support and Contributions

For support or to contribute to this project, please contact the project owner.

---
Here's the link to the project: https://hyperskill.org/projects/157

Check out my profile: https://hyperskill.org/profile/103100057
