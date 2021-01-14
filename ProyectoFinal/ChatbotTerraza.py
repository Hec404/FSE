#!/usr/bin/python
# Fecha:            13/enero/2021
# Descripción:      Programa principal de control de la terraza inteligente,
#										realiza el manejo de distintos comandos mediante un
#										chatbot de Telegram

import telebot, re
from gpiozero import LED, LEDBoard
from bluedot import BlueDot, COLORS
from random import choice
from gpiozero import PWMLED

from Atenuacion import *
from Reflectores import LedRGB, TiraLeds

# Inializacion de objetos
ledB = LEDBoard(26, 19, 13, 6, pwm=True)
lamparas = Atenuacion(ledB)

# Creacion de objeto BlueDot con 3 botones
bd = BlueDot(cols=2, rows=3)

# Ocultar botones no usados
bd[0,0].visible = False
bd[0,2].visible = False
bd[1,1].visible = False
# Cambio de colores de los botones
for button in bd.buttons:
	button.color = choice(list(COLORS.values()))

# Creación de objeto RGB
rgbObject = LedRGB(bd[1,0])

# Creación de una tira de leds
tiraLeds = TiraLeds(bd[1,2])

###Token del bot usado
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
		"Enviame la acción seguido del numero de luz.\n"+
		"Ejemplo: on 1\n"+
		"Lista de comandos reconocidos: \n" +
		"1) on: enciende la luz indicada\n" +
		"2) off: apaga la luz indicada\n" +
		"3) atenuar: usando BlueDot permite modificar la intensidad de una luz "+
		"encendida\n"+
		"4) /estado: muestra información del estado de tus luces\n\n"+
		"Uso del RGB:\n"+
		"1) /encenderRGB: Enciende el RGB y permite modificar su color mediante "+
		"el bluedot\n"+
		"2) /estableceRGB: Establece el valor del RGB para que no pueda ser "+
		"modificado por el bluedot\n"+
		"3) /apagarRGB: Apaga el RGB\n\n"
		"Uso de la tira de LEDs:\n"+
		"1) /encenderTiraLEDs: Enciende la tira de LEDs y permite manipularla "+
		"mediante el bluedot\n"+
		"2) /apagarTiraLEDs: Apaga la tira de LEDs"
	)
	return

###################################### Handlers de encendido y atenuado de luces
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

################################################################### Handlers RGB
@bot.message_handler(commands=['encenderRGB'])
def encenderRGB(message):
	if not rgbObject.get_estado(): # Si el RGB no está encendido
		# Activa el RGB
		rgbObject.control_rgb(True)
		bot.reply_to(message, "RGB activado 🎆")
	else:
		bot.reply_to(message, "El RGB ya estaba encendido 🤷")
	return

@bot.message_handler(commands=['estableceRGB'])
def estableceRGB(message):
	if rgbObject.get_estado(): # Si el RGB está encendido
		# Desactiva el control del RGB
		rgbObject.control_rgb(False)
		bot.reply_to(message, "Control del RGB desactivado 👍")
	else:
		bot.reply_to(message, 
			"Debes encender el RGB antes de establecer su color 🤷"
		)
	return

@bot.message_handler(commands=['apagarRGB'])
def apagarRGB(message):
	if rgbObject.get_estado(): # Si el RGB está encendido
		# Apaga el RGB
		rgbObject.apaga_rgb()
		bot.reply_to(message, "RGB apagado 🙈")
	else:
		bot.reply_to(message, "El RGB ya estaba apagado 🤷")
	return

########################################################## Handlers Tira de LEDs
@bot.message_handler(commands=['encenderTiraLEDs'])
def encenderTiraLEDs(message):
	if not tiraLeds.get_estado(): # Si la tira no está encendida
		# Activa la tira
		tiraLeds.enciende_tira()
		bot.reply_to(message, "Tira de LEDs activada 🚥")
	else:
		bot.reply_to(message, "La tira de LEDs ya estaba encendida 🤷")
	return

@bot.message_handler(commands=['apagarTiraLEDs'])
def apagarTiraLEDs(message):
	if tiraLeds.get_estado(): # Si la tira está encendida
		# Apaga la tira
		tiraLeds.apaga_rgb()
		bot.reply_to(message, "Tira de LEDs apagada 🙈")
	else:
		bot.reply_to(message, "La tira de LEDs ya estaba apagada 🤷")
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

bot.polling()
