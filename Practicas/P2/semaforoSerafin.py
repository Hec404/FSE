from gpiozero import LEDBoard,Button
from time import sleep

sem = LEDBoard(13, 19, 26)
button = Button(2)

def esperar():
	sem.on(2)
	button.wait_for_press(5)
	return

def verde():
	esperar()
	for i in range(3):
		sem.on(2)
		sleep(0.2)
		sem.off(2)
		sleep(0.2)
	return

def amarillo():
	sem.on(1)
	sleep(1.5)
	for i in range(3):
		sem.on(1)
		sleep(0.2)
		sem.off(1)
		sleep(0.2)
	return

def rojo():
	sem.on(0)
	sleep(3)
	sem.off(0)
	return

def semaforo():
	while True:
		verde()
		amarillo()
		rojo()

semaforo()