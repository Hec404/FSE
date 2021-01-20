import pygame
from Sensores import SensorMov

class SistemaAlarma:
	#Inicia instancia para reproducir sonidos
	pygame.mixer.init()
	pygame.mixer.music.load("bedobedo.mp3")

	def __init__(self, echo, trigger):
		self.sensor = SensorMov(echo, trigger)
		self.__alarmFlag = False
		self.__sensorFlag = True

	#Metodo para obtener el estado del sistema de alarma
	def getEstadoAlarma(self):
		return self.__alarmFlag

	#Metodo para obtener estado del sensor
	def getEstadoSensor(self):
		return self.__sensorFlag

	#Metodo para encender el sistema de alarma
	def encenderAlarma(self):
		#Comprueba estado del sistema
		if(self.getEstadoAlarma()):
			#El sistema ya estaba encendido
			return False
		else:
			#Indica el encendido del sistema
			self.__alarmFlag = True
			#Habilita el uso del sensor
			self.__sensorFlag = True
			return True

	#Metodo para desactivar el Sistema de alarma
	def desactivarAlarma(self):
		if(not self.getEstadoAlarma()):
			#El sistema se encuentra desactivado
			return False
		else:
			#Indica que se apaga el sistema
			self.__alarmFlag = False
			#Ignora el uso del sensor
			self.__sensorFlag = False
			#Apaga la alarma
			pygame.mixer.music.stop()
			return True

	#Metodo para apagar la alarma
	def apagarAlarma(self):
		if(not self.getEstadoAlarma()):
			#El sistema esta desactivado
			return 1
		#Si la alarma se activó
		elif(pygame.mixer.music.get_busy()):
			#Apaga la alarma
			pygame.mixer.music.stop()
			return 2
		#Aun no se ha activado la alarma
		else:
			return 3

	def reproducirSonido(self):
		pygame.mixer.music.play()
		return
