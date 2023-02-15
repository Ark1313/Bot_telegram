import telebot
from config import TOKEN
from extensions import GetSymbols, UserMoney, UserException

bot = telebot.TeleBot(TOKEN)
tikets = GetSymbols.get_symbols()


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = ("Привет!\n"
            "Я Бот, призван помочь тебе в конвертации валют, а то вдруг ты живёшь и не знаешь сколько рублей стоят "
            "доллары в твоём кошельке... ;) \n"
            "Шутка!\n"
            "На самом деле я могу переводить (конвертировать) энное количество одной валюты в другую "
            "согласно текущего рыночного курса.\n"
            "К сожалению я не владею всеми валютами мира (всего мне известно чуть больше 120 валют).\n"
            "Чтобы ознакомиться с актуальным списком известных мне валют набери команду /tips\n"
            "Чтобы приступить к конвертации - укажи через пробел: \n"
            "- количество имеющейся валюты,\n"
            "- 3-х буквенный код имеющейся валюты,\n"
            "- 3-х буквенный код валюты, в которой необходимо получить результат.\n"
            "Eсли не знаешь, ну или не уверен в том, как пишется этот самый код - не спеши, введи команду /tips "
            "и посмотри. Я подожду! ;) \n")
    bot.reply_to(message, text)


@bot.message_handler(commands=['tips'])
def tips(message: telebot.types.Message):
    text = ''
    for i in tikets:
        text = text + f"\n {i} : {tikets[i]}"
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def zadanie(message: telebot.types.Message):
    value = message.text.split(' ')
    try:
        amount, base, quote = message.text.split(' ')
        text = UserMoney.convert(value, amount, quote, base, tikets)
    except UserException as e:
        text = f"Ошибочка! \n {e}"
    except ValueError:
        text = f"Не знаю вкурсе ты или нет, но '{amount}' - это вообще не число!"
    except Exception as e:
        text = f"Неверное количество параметров (должно быть 3 параметра!) \n" \
              f"Почитай пожалуйста инструкцию\n" \
              f"* я надеюсь ты знаешь, что вызвать инструкцию можно командой /help \n"

    bot.reply_to(message, text)


bot.polling(none_stop=True)
