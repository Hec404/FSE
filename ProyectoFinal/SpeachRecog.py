#Es necesario instalar la biblioteca
#pip install SpeechRecognition
#importar biblioteca de reconocimiento de Voz
import speech_recognition as sr
import os
from time import sleep

from gpiozero import LED

led = LED(12)

#Crear objeto de clase Recognizer 
recognizer = sr.Recognizer()
#Definimos el ruido de los archivos, es decir valores por debajo
#se consideran silencio*/
recognizer.energy_threshold = 300

#Función para terminar ejecucuión del programa
def Fin_Program():
	#Reproducción archivo de audio
	#########FALTA GRABAR ESTE AUIDO###########
	os.system('aplay --format=S16_LE --rate=16000 fin_B.wav')
	exit()

def Reco_Voz():
	print("Tus deseos son ordenes")
	#Crea un archivo de audio wav
	#Graba durante 3 segundos 
	os.system('arecord --format=S16_LE --duration=3 --rate=16000 --file-type=wav orden.wav')
	#Detenemos el programa para permitir que termine de grabar el archivo
	#	de audio y seguir con el flujo del programa
	sleep(3.5)
	##Procesamiento de audio
	print("Procesando tu orden")
	audio_file_ = sr.AudioFile("orden.wav")

	#Casteo de archivo de audio a un tipo de dato de audio
	#Se usa el método record()
	#Offset se usa para cortar una cantidad específica de segundos 
	#		al inicio del archivo de audio


	try:
		with audio_file_ as source:
			audio_file = recognizer.record(source, offset = 1.0)
			#Usa la API web libre de Google 
			result = recognizer.recognize_google(audio_data=audio_file)
			print(result)

			#Si reconoce el comando para apagar la luz
			if(result == 'turn off lights' or result == 'turn off light' or result == 'turn off'):
				print("apagando luz")
				os.system('aplay --format=S16_LE --rate=16000 turn_off.wav')
				led.off()
				sleep(1)
			#Si reconoce el comando para prender la luz
			elif(result == 'turn on lights' or result == 'turn on light' or result == 'turn on'):
				print("prendiendo luz")
				os.system('aplay --format=S16_LE --rate=16000 turn_on.wav')
				led.on()
				sleep(3)
			#Si reconoce comando para ejecutar programa principal
			elif(result=='execute main program'):
				os.system('python3 ChatbotTerraza.py')
			#Agregar más comandos por voz para realizar diferentes acciones
			#Terminar el programa
			elif(result=='finish'):
				Fin_Program()
			#Presentar a miembros equipo
			elif(result=='present us'):
				os.system('aplay --format=S16_LE --rate=16000 equipo.wav')
			#En caso de no reconocer ninguna instrucción
			else:
				print("Lo siento, no te entendí")
				##Reproduce el archivo de audio "no_entendí"
				os.system('aplay --format=S16_LE --rate=16000 no_entendi.wav')


	except Exception as e:
		print("Lo siento, no te entendí")
		##Reproduce el archivo de audio "no_entendí"
		os.system('aplay --format=S16_LE --rate=16000 no_entendi.wav')
	else:
		pass
	finally:
		pass

# Función principal
# Se mantiene en un ciclo solicitando comandos hasta que el usuario termina
# el programa
while True:
	try:
		print('Usa Control-C para salir o envia el comando "finish"')
		input("Presiona enter para ingresar un comando de voz")
		Reco_Voz()
	except KeyboardInterrupt:
		print('Saliendo')
		exit()
