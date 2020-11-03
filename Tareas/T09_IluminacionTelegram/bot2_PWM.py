#!/usr/bin/python

import telebot
from gpiozero import LED, LEDBoard
from bluedot import BlueDot
from gpiozero import PWMLED


ledB = LEDBoard(26, 19, 13, 6, pwm=True)
lugares = (0, 1, 2, 3)
leds = []

API_TOKEN = '1364090815:AAHENBX3_jYXxLp6Fmlb5hmBDrzQU92cxug'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def encender(message):
        bot.reply_to(message, """\
Bienvenido al sistema de iluminación inteligente, \
aquí podrás apagar de manera remota las distintas luces \
de tu terraza \U0001F4A1\U0001F9E0 Envia el comando /help \
para recibir ayuda.""" """Actualmente tus luces y su estado son:
""" + estados() + """
Enviame la acción (on, off) seguido del numero de luz.\n
Ejemplo: on 1""")

# Handle '/on'
@bot.message_handler(regexp="(on){1}? [0-9]")
def encender(message):
    global l
    global leds
    l = message.text.replace("on ", "")
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
        bd.when_released = nada
        return
    if(leds[l] > 0):
        bot.reply_to(message, """\
            Esa luz ya estaba encendida, intenta atenuar \U0001F612
            """)
        bd.when_released = nada
    else:
        ledB.on(l)
        bot.reply_to(message, """\
            Se hizo la luz!!\
            """)
        bd.when_released = nada

# Handle '/off'
@bot.message_handler(regexp="(off){1}? [0-9]")
def encender(message):
    global l
    global leds
    l = message.text.replace("off ", "")
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
        bd.when_released = nada
    if(leds[l] == 0):
        bot.reply_to(message, """\
            Ya estaba morido \U0001F622""")
        bd.when_released = nada
    else:
        ledB.off(l)
        bot.reply_to(message, """\
            Se murió \U0001F61E\
            """)
        bd.when_released = nada

#Handle '/atenuar'
@bot.message_handler(regexp="(atenuar){1}? [0-9]")
def atenuar(message):
    global l
    global leds
    l = message.text.replace("atenuar ", "")
    l = int(l) - 1
    leds = ledB.value
    if(l not in lugares):
        bot.reply_to(message, """\
            Creo que no existe esa luz \U0001F605\
            """)
        bd.when_released = nada
    if(leds[l] == 0):
        bot.reply_to(message, """\
            No puedo atenuar hasta que la enciendas \U0001F622""")
        bd.when_released = nada
    else:
        
        bd.when_moved = set_brightness
        
        bot.reply_to(message, """\
            Atenuación \U0001F61C\
            """)
        print(leds[0])
        
        
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
    print(brightness)
            
def nada():
    pass



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