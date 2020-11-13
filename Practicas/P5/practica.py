# Fecha:         12/noviembre/2020
# Descripción:   Programa que utiliza un bot de telgram para seleccionar
#                diferentes modos de interactuar con los elementos de la
#                terraza inteligente.
#
#   Comando             Descripción del comando
#   /start, /help       Envia un mensaje al usuario sobre el uso del bot.
#
#   /toldo1             Permite cerrar el toldo de la terraza cuando se
#                       detecta la luz del sol, mientras que al caer la noche,
#                       se vuelve a abrir. Esto de forma automática.
#
#   /toldo2             Permite abrir y cerrar el toldo de forma manual usando
#                       un botón bluedot. Posee validación en caso de abir o
#                       cerrar el toldo en su extremo máximo.
#
#   /mov                Permite encender una lámpara de forma automática.
#                       El encendido se realiza si es de noche y se detecta una
#                       persona en la terraza.

import telebot
from gpiozero import DistanceSensor, Motor, LightSensor, LED, DistanceSensor
from time import sleep
from signal import pause
from bluedot import BlueDot

sensorLuz = LightSensor(16)
led = LED(12)
sensorUltra = DistanceSensor(14, 15, max_distance=1,threshold_distance=0.2)
motor = Motor(forward=21,backward=20)

#Variables globales 
banderaT=1
pos_ant=0
cont_for=0
cont_back=0

# Cambia el Token con el correspondiente de tu bot
API_TOKEN = '1364090815:AAHENBX3_jYXxLp6Fmlb5hmBDrzQU92cxug'
 
bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def info(message):
        bot.reply_to(message,
            "Bienvenido a la Terraza inteligente.\n"+
            "Comandos:\n"
            "</toldo1>: Automático\n"+
            "</toldo2>: Manual \n"+
            "</mov>: Detecta movimiento y prende luz \n"
        )


#Abre y cierra toldo con base a el sensor de Luz
# Handle '/toldo1'
@bot.message_handler(commands=['toldo1'])
def toldo(message):
    global banderaT

    #Si se detecta luz se cierra el toldo
    sensorLuz.when_light = light
    
    #Si no hay luz
    sensorLuz.when_dark=dark
    
    bd.when_moved = None

        
def dark():
    global banderaT
    print("Aqui")
    motor.backward()
    sleep(3)
    #Indicamos que el toldo está abierto
    banderaT=1 
    motor.stop()

def light():
    global banderaT
    print("Alla")
    motor.forward()
    sleep(3)
    #Indicamos que el toldo está abierto
    banderaT=0 
    motor.stop()



# Handle '/toldo2'
@bot.message_handler(commands=['toldo2'])
def toldo2(message):
    ##Le damos una posicion inicial al toldo
    global cont_back
    global cont_for
    cont_back=0
    cont_for=100
    bd.when_moved = set_pos
    bd.when_released = motor.stop()
   
def set_pos(pos):
    global pos_ant,cont_for,cont_back
    pos_act = pos.x
    print("back ",cont_back)
    print("for ",cont_for)
    #Si la posición actual es mayor a la anterior el abrimos
    if (pos_act>pos_ant):
        #Si avanza más de lo debido
        if(cont_back>100):
            print("Alto! Lo vas a romper")
            motor.stop()
        else:
            motor.backward()
            cont_for-=1
            cont_back+=1
     #Si la posición actual es menor a la anterior el cerramos
    elif(pos_act<pos_ant):
        #Si avanza más de lo debido
        if(cont_for>100):
            print("Alto! Lo vas a romper")
            motor.stop()
        else:
            motor.forward()
            cont_for+=1
            cont_back-=1
    #Guardamos posición anterior
    pos_ant=pos_act



# Handle '/mov'
@bot.message_handler(commands=['mov'])
def detectMov(message):
    #Sólo reacciona cuando no hay luz
    sensorLuz.when_dark = sensorMov
    #Cuando hay luz no prende el led
    sensorLuz.when_light = es_dia
    bd.when_moved = None
def sensorMov():
    sensorUltra.when_in_range = led.on
    sensorUltra.when_out_of_range = led.off
    bd.when_moved = None
    
def es_dia():
    sensorUltra.when_in_range = led.off
    sensorUltra.when_out_of_range = led.off
    bd.when_moved = None

bd = BlueDot()
    
bot.polling()    
