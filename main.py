import asyncio
import requests
import random
import time
import aiogram
from faker import Faker
from aiogram.types import InputFile
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import live

fake = Faker()

def luhn_algorithm(card_number):
    digits = [int(digit) for digit in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

async def send_messages():
    # Inicia el bot
    bot = aiogram.Bot(token='7077569483:AAHfdJIL77Y4L4Bz9iyQqw9eZ4pDKaDGOXk')
    chat_id = -6829567767

    # Lee el archivo de texto
    with open('cards.txt') as file:
        lines = file.readlines()

    # ConfiguraciÃ³n de lÃ­mite y pausa
    requests_limit = 1  # NÃºmero de solicitudes por cada pausa larga
    pause_duration = 1  # DuraciÃ³n de la pausa larga en segundos

    # Itera sobre las lÃ­neas del archivo de texto y envÃ­a cada mensaje al canal
    for i, line in enumerate(lines, start=1):
        # Elimina los Ãºltimos 4 dÃ­gitos del nÃºmero de tarjeta
        linea = line[:28]
        card_number = line[:12]

        # Verifica si la tarjeta es vÃ¡lida usando el algoritmo de Luhn
        if not luhn_algorithm(card_number):
            print(f"Tarjeta invÃ¡lida en la posiciÃ³n {i}: {linea}")
            continue

        # Verifica el bin de la tarjeta
        BIN = card_number[:6]
        req = requests.get(f"https://bins.antipublic.cc/bins/{BIN}").json()

        # Manejo del error si la clave 'brand' no estÃ¡ presente
        try:
            brand = req['brand']
        except KeyError:
            print("La clave 'brand' no estÃ¡ presente en la respuesta JSON. Se omitirÃ¡ esta entrada.")
            continue

        # Capturando los valores de la respuesta JSON
        country = req['country']
        country_name = req['country_name']
        country_flag = req['country_flag']
        country_currencies = req['country_currencies']
        bank = req['bank']
        level = req['level']
        typea = req['type']

        # Genera una fecha aleatoria en el rango de los Ãºltimos 5 aÃ±os
        month = str(random.randint(1, 12)).zfill(2)

        # Genera un aÃ±o aleatorio de dos dÃ­gitos (entre 22 y 29)
        year = str(random.randint(24, 32)).zfill(2)

        # Genera un nombre aleatorio
        full_name = fake.name()

        # Genera una direcciÃ³n aleatoria
        address = fake.address()

        # Ruta de la foto que deseas enviar
        photo_path = "LAST WARNING.jpg"

        # Carga la foto utilizando InputFile
        photo = InputFile(photo_path)

        button_consultas = InlineKeyboardButton("JOIN CHANNEL", url="https://t.me/+WeihBIn5ln9jZjE1")
        # Agrega los botones a una lista
        keyboard = [[button_consultas]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        message = ""
        message += f"\n"
        message += f" lucifer vip Scrapper V1.1 ðŸ"
        message += "â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
        message += f"<b>âŒ– ð—–ð—° â¤³</b> <code>{linea}</code>\n"
        message += f"âŒ– ð—¦ð˜ð—®ð˜ð˜‚ð˜€ â¤³ ð™‘ð˜¼ð™‡ð™„ð˜¿ð˜¼! âœ…\n"
        message += f"âŒ– ð—•ð—¶ð—» â¤³ #Bin{BIN}\n"
        message += "â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
        message += f"<b>âŒ® ð—œð—»ð—³ð—¼ â¤³ </b>  <code>{brand}-{typea}-{level}</code>\n"
        message += f"<b>âŒ® ð—•ð—®ð—»ð—°ð—¼ â¤³ </b>  <code>{bank}</code>\n"
        message += f"<b>âŒ® ð—£ð—®ð—¶ð˜€ â¤³ </b>  <code>{country_name} [{country_flag}]</code>\n"
        message += "â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
        message += f"<b>âŒ® ð„ð±ð­ð«ðš â¤³ </b>  <code>{card_number}xxxx|{month}|{year}|rnd</code>\n"
        message += f"âŒ–  cheker by â¤³ @lucifer_b0lte\n"
        message += "â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"


        # EnvÃ­a el mensaje al canal con parse_mode='HTML'
        try:
            await bot.send_photo(chat_id, photo, caption=message, reply_markup=reply_markup, parse_mode='HTML')
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")

        # Verifica si se alcanzÃ³ el lÃ­mite de solicitudes
        if i % requests_limit == 0 and i != len(lines):
            print(f"Se ha alcanzado el lÃ­mite de solicitudes. Se realizarÃ¡ una pausa de {pause_duration} segundos.")
            time.sleep(pause_duration)

live()
if __name__ == '__main__':
  asyncio.run(send_messages())
