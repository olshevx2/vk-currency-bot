import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    keys = {
        'евро': 'EUR',
        'доллар': 'USD',
        'рубль': 'RUB',
    }

    @staticmethod
    def get_price(base, quote, amount):
        base_key = base.lower()
        quote_key = quote.lower()

        if base_key not in CurrencyConverter.keys:
            raise APIException(f"Валюта '{base}' не найдена. Доступные: {', '.join(CurrencyConverter.keys)}")
        if quote_key not in CurrencyConverter.keys:
            raise APIException(f"Валюта '{quote}' не найдена. Доступные: {', '.join(CurrencyConverter.keys)}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"'{amount}' — это не число. Введите число, например 100")

        if amount <= 0:
            raise APIException("Количество должно быть больше нуля")

        base_code = CurrencyConverter.keys[base_key]
        quote_code = CurrencyConverter.keys[quote_key]

        url = f"https://open.er-api.com/v6/latest/{base_code}"
        response = requests.get(url)
        data = json.loads(response.text)

        if data.get('result') != 'success':
            raise APIException("Не удалось получить курс с сайта валют")

        rate = data['rates'][quote_code]
        result = round(rate * amount, 2)
        return result