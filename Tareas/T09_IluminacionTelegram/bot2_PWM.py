#!/usr/bin/python
# Fecha:            1/noviembre/2020
# Descripción:      Programa que permite encender, apagar y atenuar diferentes
#                   luces utilizando un bot de Telegram

import telebot, re
from gpiozero import LED, LEDBoard
from bluedot import BlueDot
from gpiozero import PWMLED


ledB = LEDBoard(26, 19, 13, 6, pwm=True)
lugares = (0, 1, 2, 3)
leds = []

#### Cambia el Token con el correspondiente de tu bot
API_TOKEN = '1258492295:AAH7DDW2U-FyzQmEqKN30METEspTYSjwaSQ'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def info(message):
        bot.reply_to(message,
            "Bienvenido al sistema de iluminación inteligente, aquí podrás "+
            "encender y apagar de manera remota las distintas luces "+
            "de tu terraza \U0001F4A1\U0001F9E0, además de poder atenuar su "+
            "intensidad.\nEnvia el comando /help para recibir ayuda.\n"+
            "Actualmente tus luces y su estado son:\n" + estados() +
            "Enviame la acción (on, off) seguido del numero de luz.\n"+
            "Ejemplo: on 1\n"+
            "Cuando la luz esté encendida, puedes enviar el mensaje 'atenuar n"+
            "' para atenuar la luz n-ésima."
        )

# Handle '/on'
@bot.message_handler(regexp="(on){1}? [0-9]")
def encender(message):
    global l
    global leds
    # expresión regular para obtener los números con mensaje case insesitive
    reg = re.compile("(on){1}? ([0-9])", re.I)
    m = reg.match(message.text)
    l = m.group(2) # Obtiene el número de la cadena recibida
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
        bd.when_moved = None
        return
    if(leds[l] > 0):
        bot.reply_to(message, """\
            Esa luz ya estaba encendida, intenta atenuar \U0001F612
            """)
        bd.when_moved = None
    else:
        ledB.on(l)
        bot.reply_to(message, """\
            Se hizo la luz!!\
            """)
        bd.when_moved = None

# Handle '/off'
@bot.message_handler(regexp="(off){1}? [0-9]")
def apagar(message):
    global l
    global leds
    reg = re.compile("(off){1}? ([0-9])", re.I)
    m = reg.match(message.text)
    l = m.group(2) # Obtiene el número de la cadena recibida
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
        bd.when_moved = None
    if(leds[l] == 0):
        bot.reply_to(message, """\
            Ya estaba morido \U0001F622""")
        bd.when_moved = None
    else:
        ledB.off(l)
        bot.reply_to(message, """\
            Se murió \U0001F61E\
            """)
        bd.when_moved = None

#Handle '/atenuar'
@bot.message_handler(regexp="(atenuar){1}? [0-9]")
def atenuar(message):
    global l
    global leds
    reg = re.compile("(atenuar){1}? ([0-9])", re.I)
    m = reg.match(message.text)
    l = m.group(2) # Obtiene el número de la cadena recibida
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
        bd.when_moved = None
    if(leds[l] == 0):
        bot.reply_to(message, """\
            No puedo atenuar hasta que la enciendas \U0001F622""")
        bd.when_moved = None
    else:
        
        bd.when_moved = set_brightness
        
        bot.reply_to(message, """\
            Atenuación \U0001F61C\
            """)

def set_brightness(pos):
    global brightness 
    brightness = (pos.y + 1) / 2
    global leds
    global l
    if (l==0):
        ledB.value =(brightness,leds[1],leds[2],leds[3])
    if (l==1):
        ledB.value =(leds[0],brightness,leds[2],leds[3])
    if (l==2):
        ledB.value =(leds[0],leds[1],brightness,leds[3])
    if (l==3):
        ledB.value =(leds[0],leds[1],leds[2],brightness)

# Maneja aquellos mensajes cuyo content_type sea 'text'
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message,
        "Comando <" + message.text + "> no encontrado\n" +
        "Envía el comando /help para obter ayuda sobre el funcionamiento del "
        "bot \U0001F916"
    )

# Función que permite mostrar el estado de las lámparas. Es decir, si están
# encendidas o apagadas.
def estados():
    est = ""
    leds = ledB.value
    for i in range(len(leds)):
        if(leds[i] == 0):
            est += str(i+1)+" \U000026AB\n"
        else:
            est += str(i+1)+" \U0001F4A1\n"
    return est

bd = BlueDot()
bot.polling()