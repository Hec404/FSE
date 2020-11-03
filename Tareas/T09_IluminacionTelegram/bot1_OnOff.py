#!/usr/bin/python
# Fecha:            27/octubre/2020
# Descripción:      Programa que permite encender y apagar diferentes luces
#                   utilizando un bot de Telegram

import telebot, re
from gpiozero import LED, LEDBoard

ledB = LEDBoard(26, 19, 13, 6)
lugares = (0, 1, 2, 3)

API_TOKEN = '1258492295:AAH7DDW2U-FyzQmEqKN30METEspTYSjwaSQ'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def info(message):
        bot.reply_to(message, """\
Bienvenido al sistema de iluminación inteligente, \
aquí podrás apagar de manera remota las distintas luces \
de tu terraza \U0001F4A1\U0001F9E0.\n""" +
"""Envia el comando /help para recibir ayuda.\n""" +
"""Actualmente tus luces y su estado son:
""" + estados() + """
Enviame la acción (on, off) seguido del numero de luz.\n
Ejemplo: on 1""")

# Handle '/on'
@bot.message_handler(regexp="(on){1}? ([0-9])")
def encender(message):
    reg = re.compile("(on){1}? ([0-9])", re.I)
    m = reg.match(message.text)
    l = m.group(2) # Obtiene el número de la cadena recibida
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
        return
    if(leds[l] == 1):
        bot.reply_to(message, """\
            Esa luz ya estaba encendida \U0001F612
            """)
    else:
        ledB.on(l)
        bot.reply_to(message, """\
            Se hizo la luz!!\
            """)

# Handle '/off'
@bot.message_handler(regexp="(off){1}? [0-9]")
def apagar(message):
    reg = re.compile("(off){1}? ([0-9])", re.I)
    m = reg.match(message.text)
    l = m.group(2) # Obtiene el número de la cadena recibida
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
    if(leds[l] == 0):
        bot.reply_to(message, """\
            Ya estaba morido \U0001F622""")
    else:
        ledB.off(l)
        bot.reply_to(message, """\
            Se murió \U0001F61E\
            """)

# Handle all other messages with content_type 'text' (content_types defaults to
# ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, """\
    Comando <""" + message.text + "> no encontrado\n" +
    "Envia el comando /help para obter ayuda sobre el funcionamiento del bot " +
    "\U0001F916"
    )

def estados():
    est = ""
    leds = ledB.value
    for i in range(len(leds)):
        if(leds[i] == 0):
            est += str(i+1)+" \U000026AB\n"
        else:
            est += str(i+1)+" \U0001F4A1\n"
    return est

bot.polling()