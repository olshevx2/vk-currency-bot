import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import VK_TOKEN
from extensions import APIException, CurrencyConverter

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def send_message(user_id, message):
    vk.messages.send(user_id=user_id, message=message, random_id=0)


HELP = (
    "Привет! Я бот-конвертер валют \n\n"
    "Напиши мне в формате:\n"
    "<валюта 1> <валюта 2> <количество>\n\n"
    "Пример: евро доллар 100\n\n"
    "Команды:\n"
    "/values — какие валюты я знаю\n"
    "/help — эта справка"
)


print("Бот запущен...")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        text = event.text.strip()
        low = text.lower()

        if low in ['/start', '/help']:
            send_message(user_id, HELP)

        elif low == '/values':
            values = ', '.join(CurrencyConverter.keys)
            send_message(user_id, f"Доступные валюты: {values}")

        else:
            try:
                # ждём три слова: валюта1 валюта2 количество
                parts = text.split()
                if len(parts) != 3:
                    raise APIException(
                        "Введите в формате: <валюта 1> <валюта 2> <количество>\n"
                        "Пример: евро доллар 100"
                    )

                base, quote, amount = parts
                result = CurrencyConverter.get_price(base, quote, amount)
                send_message(user_id, f"{amount} {base} = {result} {quote}")

            except APIException as e:
                # наша ошибка — показываем текст
                send_message(user_id, f"Ошибка: {e}")

            except Exception as e:
                # любая другая ошибка — тоже показываем с типом (пункт 9)
                send_message(user_id, f"Ошибка {type(e).__name__}: {e}")