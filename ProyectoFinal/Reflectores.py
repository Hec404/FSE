#!/usr/bin/python
# Fecha:            13/Enero/2021
# Descripción:      Contiene funciones para el control de un LED RGB y una tira
#                   de LEDs usando bluedot

from gpiozero import LEDBoard, exc
from math import sqrt

# Atenuación
# Usada para representar a un objeto RGB

class LedRGB:
  # Constructor de la clase
  def __init__(self, bluedot):
    # bluedot es una instancia de bluedot.BlueDot
    self.__bluedot = bluedot
    #          Colores  R   G   B
    self.__led = LEDBoard(21, 20, 16, pwm=True)
    # Bandera para saber si el LED está encendido
    self.__encendido = False

  # Método que permite asignar atenuaciones distintas a cada componente del RGB
  def set_rgb_color(self,pos):
    try:
      # R
      self.__led[0].value = - ((sqrt((pos.x**2) + ((pos.y-1)**2)))/2) + 1
      # G
      self.__led[1].value = - \
          ((sqrt(((pos.x-0.866)**2) + ((pos.y+0.5)**2)))/2) + 1
      # B
      self.__led[2].value = - \
          ((sqrt(((pos.x+0.866)**2) + ((pos.y+0.5)**2)))/2) + 1
    except exc.OutputDeviceBadValue as value:
      pass
    

  # Método para que permite controlar cuando activar el control del RGB
  # por el bluedot
  def control_rgb(self,active):
    self.__encendido = True
    if active:
      self.__bluedot.when_moved = self.set_rgb_color
    else:
      self.__bluedot.when_moved = None

  # Método para apagar el RGB
  def apaga_rgb(self):
    self.__encendido = False
    self.__bluedot.when_moved = None
    for color in self.__led:
      color.value = 0

  # Método para obtener el estado del RGB (encendido o apagado)
  def get_estado(self):
    return self.__encendido
