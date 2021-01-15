#!/usr/bin/python
# Fecha:            14/Enero/2021
# Descripción:   Programa que utiliza un bot de telgram para seleccionar
#                diferentes modos de interactuar con los elementos de la
#                terraza inteligente.
#
#   Comando             Descripción del comando
#   /start, /help       Envia un mensaje al usuario sobre el uso del bot.
#
#   /toldo1             Permite cerrar el toldo de la terraza cuando se
#                       detecta la luz del sol, mientras que al caer la noche,
#                       se vuelve a abrir. Esto de forma automática.
#
#   /toldo2             Permite abrir y cerrar el toldo de forma manual usando
#                       un botón bluedot. Posee validación en caso de abir o
#                       cerrar el toldo en su extremo máximo.
#
#   /mov                Permite encender una lámpara de forma automática.
#                       El encendido se realiza si es de noche y se detecta una
#                       persona en la terraza.

import telebot, re
from gpiozero import DistanceSensor, Motor, LightSensor, LED, DistanceSensor
from time import sleep
from signal import pause
from bluedot import BlueDot

 
class SensorLuz:
    #Consrtuctor de la clase
    def __init__(self,ledSL):
        self.sensorLuz = ledSL
        self.valor = 0

    #Metodo para obtener el valor del sensor
    def getValor(self):
        if (self.sensorLuz.when_dark):
            return 0
        elif (self.sensorLuz.when_light):
            return 1
        else:
            return -1

    def getEstado(self):
        est = ""
        v=self.getValor()
        #Comprobando el valor del sensor
        if(v == 0):
            est +=  "Es de noche"+" \U0001F31A\n"
        if(v == 1):
            est +=  "Es de día"+" \U0001F31E\n"
        else:
            est +=  "Error con el sensor. Dar mantenimiento"+" \U00002699\n"


class SensorMov:
     #Consrtuctor de la clase
    def __init__(self):
        self.sensorUltra = DistanceSensor(14, 15, max_distance=1,threshold_distance=0.2)
        self.valor = 0

    def getRange(self):
        if (self.sensorUltra.when_in_range):
            return 1
        elif (self.sensorUltra.when_out_of_range):
            return 0
        else:
            return -1

class Motor_P:
    #Constructor de la clase:
    def __init__(self, bluedot):
        self.motor = Motor(forward=21,backward=20)
        # bluedot es una instancia de bluedot.BlueDot
        self.__bluedot = bluedot
        self.cont_back = 0
        self.cont_for = 0
        self.pos_ant=0


    def __set_pos(self,pos):
        pos_act = pos.x
         #Si la posición actual es mayor a la anterior el abrimos
        if (pos_act > self.pos_ant):
            #Si avanza más de lo debido
            if(self.cont_back>100):
                print("Alto! Lo vas a romper")
                motor.stop()
            else:
                motor.backward()
                self.cont_for-=1
                self.cont_back+=1
         #Si la posición actual es menor a la anterior el cerramos
        elif(pos_act<self.pos_ant):
            #Si avanza más de lo debido
            if(self.cont_for>100):
                print("Alto! Lo vas a romper")
                motor.stop()
            else:
                motor.forward()
                self.cont_for+=1
                self.cont_back-=1
        #Guardamos posición anterior
        self.pos_ant=pos_act
        

