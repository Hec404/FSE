#!/usr/bin/python
# Fecha:            08/Enero/2021
# Descripción:      Programa que permite encender, apagar y atenuar diferentes
#                   luces de la terraza

import telebot, re
from gpiozero import LED, LEDBoard
from bluedot import BlueDot
from gpiozero import PWMLED

class Atenuacion():
	#Constructor de la clase
	def __init__(self, ledB):
		#Asigna LEDBoard pasado como parametro
		self.ledB = ledB
		self.lugares = (0, 1, 2, 3)
		self.leds = []
		self.brillo = 0

	#Metodo para obtener lista de valores de leds
	def getValores(self):
		self.leds = self.ledB.value
		return

	#Metodo para obtener el estado de las lamparas. Si estan encendidas o apagadas
	def getEstados(self):
		est = "Actualmente tus luces y su estado son:\n"
		self.getValores()
		#Recorre lista de valores de leds
		for i in range(len(self.leds)):
			#Comprobacion del estado de cada led
			if(self.leds[i] == 0):
				est += str(i+1) + " \U000026AB\n"
			else:
				est += str(i+1) + " \U0001F4A1\n"
		return est

	#Metodo para convertir lugar a entero
	def convertirLugar(self, cadena):
		return (int(cadena) - 1)

	#Metodo para verificar la existencia de un lugar
	def comprobarLugares(self, lugar):
		l = self.convertirLugar(lugar)
		if(l not in self.lugares):
			return True

	#Metodo para apagar una luz
	def apagarLuz(self, lugar):
		l = self.convertirLugar(lugar)
		#Obtiene valores de los leds
		self.getValores()
		#Comprueba si el led esta apagado
		if(self.leds[l] == 0):
			return False
		else:
			#Apaga el led indicado
			self.ledB.off(l)
			return True

	#Metodo para encender una luz
	def encenderLuz(self, lugar):
		l = self.convertirLugar(lugar)
		#Obtiene valores de los leds
		self.getValores()
		#Comprueba si el led esta encendido
		if(self.leds[l] > 0):
			return False
		else:
			self.ledB.on(l)
			return True

	#Metodo para la atenuacion de una luz
	def atenuarLuz(self, lugar):
		l = self.convertirLugar(lugar)
		#Obtiene valores de los leds
		self.getValores()
		#Comprueba si el led esta apagado
		if(self.leds[l] == 0):
			return False
		else:
			#Ajusta el valor de la atenuacion del led seleccionado
			if(l == 0):
				self.ledB.value = (self.brillo, self.leds[1], self.leds[2], self.leds[3])
			if(l == 1):
				self.ledB.value = (self.leds[0], self.brillo, self.leds[2], self.leds[3])
			if(l == 2):
				self.ledB.value = (self.leds[0], self.leds[1], self.brillo, self.leds[3])
			if(l == 3):
				self.ledB.value = (self.leds[0], self.leds[1], self.leds[2], self.brillo)
			return True

	def ajustarAtenuacion(self, pos):
		self.brillo = (pos.y + 1) / 2
		#return self.brillo