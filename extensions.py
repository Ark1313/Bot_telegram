import json
import requests
from config import headers


class GetSymbols:
    @staticmethod
    def get_symbols():  # метод получения типов валют, поддерживаемых сайтом
        url = "https://api.apilayer.com/exchangerates_data/symbols"
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        result = json.loads(response.text)
        result = result['symbols']
        return result


class UserException(Exception):     # класс исключений
    pass


class UserMoney:  # класс получающий входные данные
    # - имя валюты, цену на которую надо узнать, — base;
    # - имя валюты, цену в которой надо узнать, — quote;
    # - количество переводимой валюты — amount.

    @staticmethod
    def get_price(amount, base, quote):     # Запрос на конвертацию

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote}&from={base}&amount={amount}"
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        result = json.loads(response.text)
        return result['result']

    @staticmethod
    def chek(value, amount, quote, base, tikets):    # метод проверки значений
        if len(value) != 3:
            raise UserException("Неверное количество параметров (должно быть 3 параметра!) \n"
                                "Почитай пожалуйста инструкцию\n"
                                "* я надеюсь ты знаешь, что вызвать инструкцию можно командой /help ")
        if quote == base:
            raise UserException("А чего это у нас валюты одинаковые?\n"
                                "я надеюсь это ошибка, а не дикое желание поглумиться над искусственным "
                                "интелектом...\n"
                                "ты смотри, я ведь могу и пожаловаться куда надо! "
                                "Благо сейчас всё можно сделать через Интрнет ;)")
        if float(amount) <= 0:
            raise UserException("Ну, и для чего ты вводишь отрицательную сумму денег?\n"
                                "Неужели надеешься, что обменный пункт пожалеет тебя и даст тебе своих денег???\n"
                                "xDDD")
        if base not in tikets:
            raise UserException(f"ОЙ! А что это за валюта такая {base}? Давай попробуем ещё раз!")
        if quote not in tikets:
            raise UserException(f"ОЙ! А что это за валюта такая {quote}? Давай попробуем ещё раз!")


    @staticmethod
    def convert(value, amount, quote, base, tikets):    # метод конвертации
        UserMoney.chek(value, amount, quote, base, tikets)
        result = UserMoney.get_price(amount, base, quote)
        print(result)
        text = f"{amount} {base} = {result} {quote}"
        return text

