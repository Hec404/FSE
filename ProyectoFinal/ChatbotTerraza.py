#!/usr/bin/python
# Fecha:            1/noviembre/2020
# Descripción:      Programa principal de control de la terraza inteligente,
#					realiza el manejo de distintos comandos mediante un
#					chatbot de Telegram

import telebot, re
from gpiozero import LED, LEDBoard
from bluedot import BlueDot, COLORS
from random import choice
from gpiozero import PWMLED

from Atenuacion import *

#Inializacion de objetos
ledB = LEDBoard(26, 19, 13, 6, pwm=True)
lamparas = Atenuacion(ledB)

###Token del bot usado
API_TOKEN = '1391144634:AAHEamkwuK8dOQ-oYpEPn59fiBXzGGkq-uA'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def info(message):
    bot.reply_to(message,
        "Bienvenido al sistema de iluminación inteligente, aquí podrás "+
        "encender y apagar de manera remota las distintas luces "+
        "de tu terraza \U0001F4A1\U0001F9E0, además de poder atenuar su "+
        "intensidad.\nEnvia el comando /help para recibir ayuda.\n"+
        "Enviame la acción seguido del numero de luz.\n"+
        "Ejemplo: on 1\n"+
        "Lista de comandos reconocidos: \n" +
        "1) on: enciende la luz indicada\n" +
        "2) off: apaga la luz indicada\n" +
        "3) atenuar: usando BlueDot permite modificar la intensidad de una luz encendida\n" +
        "4) /estado: muestra información del estado de tus luces"
    )
    return

#handle '/estado'
@bot.message_handler(commands=['estado'])
def estadoLuces(message):
	global lamparas
	bot.reply_to(message, lamparas.getEstados())
	return

#Handle '/on'
@bot.message_handler(regexp = "(on){1}? [0-9]")
def botEncenderLuz(message):
	global lamparas
	#Expresion regular para obtener numeros con mensajes case insesitive
	# "(on){1}? ([0-9])
	#Obtiene el numero de la cadena recibida
	l = obtenerNumero("(on){1}? ([0-9])", message)
	#Comprueba si el lugar recibido no existe
	if(lamparas.comprobarLugares(l)):
		bot.reply_to(message, """\
			Creo que no existe esa luz \U0001F605 """)
		return
	#Llamada metodo para encender una luz
	if(lamparas.encenderLuz(l)):
		bot.reply_to(message, """\
			Se hizo la luz!!""")
		return
	else:
		#No se encendió la luz seleccionada
		bot.reply_to(message, """\
			Esa luz ya estaba encendida, intenta atenuar \U0001F612 """)
		return

#Handle '/off'
@bot.message_handler(regexp = "(off){1}? [0-9]")
def botApagarLuz(message):
	global lamparas
	#Obtiene el numero de la cadena recibida
	l = obtenerNumero("(off){1}? ([0-9])", message)
	#Comprueba si el lugar recibido no existe
	if(lamparas.comprobarLugares(l)):
		bot.reply_to(message, """\
			Creo que no existe esa luz \U0001F605 """)
		return
	#Llamada al metodo para apagar una luz
	if(lamparas.apagarLuz(l)):
		bot.reply_to(message, """\
			Se murió \U0001F61E """)
		return
	else:
		#No se apagó la luz seleccionada
		bot.reply_to(message, """\
			Ya estaba morido \U0001F622 """)
		return

#Handle '/atenuar'
@bot.message_handler(regexp = "(atenuar){1}? [0-9]")
def botAtenuarLuz(message):
	global lamparas
	l = obtenerNumero("(atenuar){1}? ([0-9])", message)
	#Comprueba si el lugar recibido no existe
	if(lamparas.comprobarLugares(l)):
		bot.reply_to(message, """\
			Creo que no existe esa luz \U0001F605 """)
		return
	#Llama al metodo para atenuar una luz
	if(lamparas.atenuarLuz(l)):
		#Asocia funcion a BlueDot
		bd[0,1].when_moved = lamparas.ajustarAtenuacion
		bot.reply_to(message, """\
			Atenuación \U0001F61C """)
		return
	else:
		#No se atenuó ninguna luz
		bot.reply_to(message, """\
			No puedo atenuar hasta que la enciendas \U0001F622 """)
		return

#Maneja aquellos mensajes cuyo content_type sea 'text'
@bot.message_handler(func=lambda message: True)
def echo_message(message):
	bot.reply_to(message,
		"Comando <" + message.text + "> no encontrado\n" +
		"Envía el comando /help para obtener ayuda sobre el funcionamiento del " +
		"bot \U0001F916")
	return

#Funcion para obtener numeros de los comandos a traves de una expresion regular
def obtenerNumero(expReg, mensaje):
	#Expresion regular para obtener numeros con mensajes case insesitive
	reg = re.compile(expReg, re.I)
	m = reg.match(mensaje.text)
	#Retorna el numero de la cadena recibida
	return m.group(2)

#Creacion de objeto BlueDot con 3 botones
bd = BlueDot(cols=2, rows=3)
#Ocultar botones no usados
bd[0,0].visible = False
bd[0,2].visible = False
bd[1,1].visible = False
#Cambio de colores de los botones
for button in bd.buttons:
	button.color = choice(list(COLORS.values()))

bot.polling()