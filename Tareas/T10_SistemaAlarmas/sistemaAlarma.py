#!/usr/bin/python
# Fecha:            6/noviembre/2020
# Descripción:      Programa que activa una alarma usando un sensor
#                   ultrasónico y notifica a través de un bot de Telegram

import telebot, pygame
from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=18, trigger=17, max_distance=1)

#inicia la instancia para reproducir sonidos
pygame.mixer.init()
pygame.mixer.music.load("bedobedo.mp3")
#Bandera que indica si el sistema está encendido o apagado
alarmFlag = False
#Bandera para ignorar al sensor cuando esté apagado el sistema
sensorFlag = True

# Cambia el Token con el correspondiente de tu bot
API_TOKEN = '1258492295:AAH7DDW2U-FyzQmEqKN30METEspTYSjwaSQ'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def info(message):
        bot.reply_to(message,
            "Bienvenido al sistema de alarma.\n"+
            "Comandos:\n"
            "</on>: Activa el sistema de alarma\n"+
            "</off>: Desactiva el sistema de alarma\n"+
            "</shutdown>: Apaga la alarma, sin desactivar el sistema\n"
        )

# Handle '/on'
@bot.message_handler(commands=['on'])
def encender(message):
    global alarmFlag, sensorFlag
    
    #Si el sistema ya estaba encendido
    if(alarmFlag):
        bot.reply_to(message, """\
            El sistema de alarma ya está encendido\
            """)
    #Si el sistema estaba apagado
    else:
        #Indica que se enciende el sistema
        alarmFlag = True
        #Permite el uso del sensor
        sensorFlag = True
        bot.reply_to(message, """\
            Se ha activado el sistema de alarma\
            """)
        #Espera a que se active la alarma
        setAlarm(message)

# Handle '/off'
@bot.message_handler(commands=['off'])
def apagar(message):
    global alarmFlag, sensorFlag
    
    #Si el sistema ya estaba apagado
    if(not alarmFlag):
        bot.reply_to(message, """\
            El sistema de alarma ya está apagado\
            """)
    #Si el sistema estaba encendido
    else:
        #Indica que se apaga el sistema
        alarmFlag = False
        #Ignora el uso del sensor
        sensorFlag = False
        #Apaga la alarma
        pygame.mixer.music.stop()
        #buzzer.off()
        bot.reply_to(message, """\
            PRECAUCIÓN: Se ha desactivado el sistema de alarma\
            """)

# Handle '/shutdown'
@bot.message_handler(commands=['shutdown'])
def apagarAlarma(message):
    global alarmFlag, sensorFlag
    
    #Si el sistema está apagado
    if(not alarmFlag):
        bot.reply_to(message, """\
            El sistema de alarma no está encendido\
            """)
    #elif(buzzer.is_active):
        #buzzer.off()
    #Si se activó la alarma
    elif(pygame.mixer.music.get_busy()):
        #Apaga la alarma
        pygame.mixer.music.stop()
        bot.reply_to(message, 
            "Alarma apagada\n" +
            "Verifique quién ha utilizado la puerta\n")
        #Espera a que se active la alarma
        setAlarm(message)
    #Si aún no se ha activado la alarma
    else:
        bot.reply_to(message, """\
            Aún no se ha detectado el uso de la puerta\
            """)

def setAlarm(message):
    #Espera a que se active el sensor
    sensor.wait_for_in_range()
    #Verifica si se debe ignorar el sensor, en caso de que
    #esté apagado el sistema
    if(sensorFlag):
        #Enciende la alarma
        pygame.mixer.music.play()
        #buzzer.on()
        bot.send_message(message.chat.id,"Advertencia: Alguien abrió la puerta")
    return

# Maneja aquellos mensajes cuyo content_type sea 'text'
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message,
        "Comando <" + message.text + "> no encontrado\n" +
        "Envía el comando /help para obtener ayuda sobre el funcionamiento del "
        "bot \U0001F916"
    )

bot.polling()