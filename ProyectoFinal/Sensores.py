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
    def __init__(self):
        self.__sensorLuz = LightSensor(18)
        self.valor = 0

    #Metodo para obtener el valor del sensor
    def getValor(self):
        self.__sensorLuz.when_dark = self.oscuro
        self.__sensorLuz.when_light = self.luz
        return self.valor

    def oscuro(self):
        self.valor = 0 
         
    def luz(self):
        self.valor = 1

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

#Clase para el uso de Sensores de movimiento
class SensorMov:
     #Consrtuctor de la clase
    def __init__(self, echo, trigger):
        self.sensorUltra = DistanceSensor(echo, trigger, max_distance=1,threshold_distance=0.2)
        self.valor = 0

    def getRange(self):
        self.sensorUltra.when_in_range = self.in_range
        self.sensorUltra.when_out_of_range = self.out_range
        return self.valor
        
    def in_range(self):
        self.valor = 1

    def out_range(self):
        self.valor = 0

    def wait(self):
        self.sensorUltra.wait_for_in_range()
        return

#Clase para el uso de un Motor DC
class Motor_P:
    #Constructor de la clase:
    def __init__(self, bluedot):
        self.motor = Motor(forward=23,backward=24)
        # bluedot es una instancia de bluedot.BlueDot
        self.__bluedot = bluedot
        self.cont_back = 0
        self.cont_for = 0
        self.pos_ant=0

    def atras(self):
        self.motor.backward()

    def adelante(self):
        self.motor.forward()

    def alto(self):
        self.motor.stop()

    def set_pos(self,pos):
        pos_act = pos.x
        est = ""
         #Si la posición actual es mayor a la anterior el abrimos
        if (pos_act > self.pos_ant):
            #Si avanza más de lo debido
            if(self.cont_back>100):
                self.motor.stop()
                est = "Alto! Lo vas a romper \U0001F6D1"
            else:
                self.motor.backward()
                self.cont_for-=1
                self.cont_back+=1
         #Si la posición actual es menor a la anterior el cerramos
        elif(pos_act<self.pos_ant):
            #Si avanza más de lo debido
            if(self.cont_for>100):
                self.motor.stop()
                est = "Alto! Lo vas a romper \U0001F6D1"
            else:
                self.motor.forward()
                self.cont_for+=1
                self.cont_back-=1
        #Guardamos posición anterior
        self.pos_ant=pos_act
        return est
        

