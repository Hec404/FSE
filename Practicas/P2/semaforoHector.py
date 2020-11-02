from gpiozero import Button,LEDBoard
from time import time, sleep

#Orden LEDs -> R A V
semaforo = LEDBoard(13, 19, 26)
boton = Button(2)
tiempoActual = time()
tiempoAnterior = 0

semaforo.value = (0, 0, 1)

def cambioEstado():
	global tiempoAnterior
	global tiempoActual
	cont = 0
	espera = 0.1
	
	if semaforo.value == (0, 0, 1):
		while cont <= 8:
			if (boton.is_pressed) and (tiempoActual - tiempoAnterior > 30):
				btnPress()
				return
			sleep(espera)
			cont += espera
			tiempoActual = time()
		semaforo.value = (0, 0, 0)
		sleep(1)
		semaforo.value = (0, 0, 1)
		sleep(1)
		semaforo.value = (0, 0, 0)
		sleep(1)
		semaforo.value = (0, 0, 1)
		sleep(1)
		semaforo.value = (0, 0, 0)
		sleep(1)
		semaforo.value = (0, 0, 1)
		sleep(1)
		semaforo.value = (0, 1, 0)
		return
	elif semaforo.value == (0, 1, 0):
		sleep(4)
		semaforo.value = (1, 0, 0)
		return
	elif semaforo.value == (1, 0, 0):
		sleep(6)
		semaforo.value = (0, 0, 1)
		return

def btnPress():
	print("Boton fue presionado")
	sleep(2)
	semaforo.value = (0, 0, 0)
	sleep(1)
	semaforo.value = (0, 0, 1)
	sleep(1)
	semaforo.value = (0, 0, 0)
	sleep(1)
	semaforo.value = (0, 0, 1)
	sleep(1)
	semaforo.value = (0, 0, 0)
	sleep(1)
	semaforo.value = (0, 0, 1)
	sleep(1)
	semaforo.value = (0, 1, 0)
	global tiempoAnterior
	global tiempoActual
	tiempoAnterior = tiempoActual
	tiempoActual = time()
	return

def main():
	while True:
		cambioEstado()

main()