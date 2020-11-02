from bluedot import BlueDot
from gpiozero import LEDBoard
from time import sleep
from signal import pause

#Barra de leds
leds = LEDBoard(6, 11, 0, 5, 19, 26, 13)

def sera():
    leds.value = (1, 0, 1, 1, 0, 1, 1) #S
    sleep(0.5)
    leds.value = (1, 0, 0, 1, 1, 1, 1) #E
    sleep(0.5)
    leds.value = (0, 0, 0, 0, 1, 0, 1) #R
    sleep(0.5)
    leds.value = (1, 1, 1, 0, 1, 1, 1) #A
    sleep(0.5)
    leds.value = (1, 0, 0, 0, 1, 1, 1) #F
    sleep(0.5)
    leds.value = (0, 1, 1, 0, 0, 0, 0) #I
    sleep(0.5)
    leds.value = (0, 0, 1, 0, 1, 0, 1) #N
    sleep(0.5)
    leds.off()
    

def hector():
    leds.value = (0, 1, 1, 0, 1, 1, 1) #H
    sleep(0.5)
    leds.value = (1, 0, 0, 1, 1, 1, 1) #E
    sleep(0.5)
    leds.value = (1, 0, 0, 1, 1, 1, 0) #C
    sleep(0.5)
    leds.value = (1, 1, 1, 0, 0, 0, 0) #T
    sleep(0.5)
    leds.value = (1, 1, 1, 1, 1, 1, 0) #O
    sleep(0.5)
    leds.value = (0, 0, 0, 0, 1, 0, 1) #R
    sleep(0.5)
    leds.off()

def sandra():
    leds.value = (1, 0, 1, 1, 0, 1, 1) #S
    sleep(0.5)
    leds.value = (1, 1, 1, 0, 1, 1, 1) #A
    sleep(0.5)
    leds.value = (0, 0, 1, 0, 1, 0, 1) #N
    sleep(0.5)
    leds.value = (0, 1, 1, 1, 1, 0, 1) #D
    sleep(0.5)
    leds.value = (0, 0, 0, 0, 1, 0, 1) #R
    sleep(0.5)
    leds.value = (1, 1, 1, 0, 1, 1, 1) #A
    sleep(0.5)
    leds.off()

def mario():
    leds.value = (0, 0, 1, 0, 1, 0, 1) #M
    sleep(0.5)
    leds.value = (1, 1, 1, 0, 1, 1, 1) #A
    sleep(0.5)
    leds.value = (0, 0, 0, 0, 1, 0, 1) #R
    sleep(0.5)
    leds.value = (0, 1, 1, 0, 0, 0, 0) #I
    sleep(0.5)
    leds.value = (1, 1, 1, 1, 1, 1, 0) #O
    sleep(0.5)
    leds.off()
    
def dpad(pos):
    if pos.top:
        sera()
    elif pos.bottom:
        hector()
    elif pos.right:
        sandra()
    elif pos.left:
        mario()

bd = BlueDot()
bd.when_pressed = dpad

pause()