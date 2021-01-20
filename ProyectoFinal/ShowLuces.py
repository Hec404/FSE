import subprocess, os

#Pines ocupados 2,3,4,5,9,10,11,12

class ShowLuces:
  #Constructor de la clase
  def __init__(self, tiraLeds, leds):
    #Bandera que indica si el show de luces está encendido o apagado
    self.LSPFlag = False
    self.tiraLeds = tiraLeds
    self.leds = leds
    self.proceso = None

  def apagaTira(self):
    if self.tiraLeds.get_estado(): # Si la tira está encendida
      #Apaga la tira
      self.tiraLeds.apaga_rgb()
    return

  def apagaLeds(self):
    #Apaga cada lámpara
    for i in range(4):
    	self.leds.off(i)
    return

  def getEstado(self):
  	return self.LSPFlag

  def showON(self):
  	self.LSPFlag = True
  	#Se ejecuta el programa synchronized_lights.py en un subproceso
  	#self.proceso = subprocess.Popen(['sudo','python','/home/pi/lightshowpi/py/synchronized_lights.py'])
  	self.proceso = os.system('sudo python /home/pi/lightshowpi/py/synchronized_lights.py')
  	return

  def showOFF(self):
    #Indica que se apaga el show de luces
    self.LSPFlag = False
    print("\nFinalizando LightShowPi\n")
    #Termina el subproceso del programa synchronized_lights.py
    #self.proceso.send_signal(signal.SIGINT)
    return
