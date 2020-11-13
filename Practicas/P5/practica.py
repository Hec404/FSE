import telebot
from gpiozero import DistanceSensor
from gpiozero import Motor
from gpiozero import LightSensor, LED
from gpiozero import DistanceSensor, LED
from time import sleep
from signal import pause
from bluedot import BlueDot

#
sensorLuz = LightSensor(16)
led = LED(12)
sensorUltra = DistanceSensor(14, 15, max_distance=1,threshold_distance=0.2)
motor = Motor(forward=21,backward=20)

#Bandera para toldo, considera que está cerrada inicialmente
banderaT=1
pos_ant=0

# Cambia el Token con el correspondiente de tu bot
API_TOKEN = '1364090815:AAHENBX3_jYXxLp6Fmlb5hmBDrzQU92cxug'
 
bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def info(message):
        bot.reply_to(message,
            "Bienvenido a la Terraza inteligente.\n"+
            "Comandos:\n"
            "</on>: Activa el sistema \n"+
            "</off>: Desactiva el sistema\n"+
            "</toldo1>: Automático\n"+
            "</toldo2>: Manual \n"+
            "</mov>: Detecta movimiento y prende luz \n"
        )


#Abre y cierra toldo con base a el sensor de Luz
# Handle '/toldo1'
@bot.message_handler(commands=['toldo1'])
def toldo(message):
    global banderaT
    #Si no se detecta luz se abre el toldo
    print(banderaT)
    print(sensorLuz.value)
    #Si el toldo está cerrado
#    if (banderaT==0):
#        bot.reply_to(message, 
#            "Está atardeciendo\n" +
#            "Dejemos entrar la luz \n")
#        sensorLuz.when_dark = dark
#        bd.when_moved = None
        #sensorLuz.when_light = nada
    #Si el toldo está abierto
 #   else:
 #       bot.reply_to(message, 
  #          "Hay mucho Sol\n" +
 #           "Cuidemos tu piel\n")
        #Si se detecta luz se cierra el toldo
 #       sensorLuz.when_light = light
  #      bd.when_moved = None
    #Si no hay luz
    sensorLuz.when_dark=dark
        
    sensorLuz.when_light=light
        
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
    bd.when_moved = set_pos
    bd.when_released = nada
    
   
def set_pos(pos):
    global pos_ant
    pos_act = pos.x
    if (pos_act>pos_ant):
        motor.backward()
    elif(pos_act<pos_ant):
        motor.forward()
    pos_ant=pos_act
    
    
def nada():
    motor.stop()
#Si no hay luz prende el led si detecta la presencia de alguien
# Handle '/mov'
@bot.message_handler(commands=['mov'])
def detectMov(message):
    sensorLuz.when_dark = sensorMov
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

def mensajes(message,x):
    bot.reply_to(message, 
            "El camino es oscuro\n" +
            "Alumbremos a los paseantes\n")
    
    
bd = BlueDot()
    
bot.polling()    
