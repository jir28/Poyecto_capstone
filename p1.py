
import RPi.GPIO as GPIO #puertos de raspberry
import time
#from w1thermsensor import W1ThermSensor #libreria para sensor de temperatura de agua
from yeelight import Bulb#Libreria para foco MI

f = open('flowmeter.txt','a')
bulb = Bulb("192.168.3.28")

GPIO.setmode(GPIO.BCM)
inpt = 13
GPIO.setup(inpt,GPIO.IN)
minutos = 0
constant = 0.00210
time_new = 0.0
rpt_int = 10

global rate_cnt, tot_cnt,TotLit,LperM,tiempo,aux
rate_cnt = 0
tot_cnt = 0
aux = 0

def Pulse_cnt(inpt_pin):
    global rate_cnt, tot_cnt
    rate_cnt +=1
    tot_cnt +=1
    
GPIO.add_event_detect(inpt,GPIO.FALLING,callback=Pulse_cnt)

#MAIN
print("Registro de litros gastados y temperatura promedio el dia: ",str(time.asctime(time.localtime(time.time()))))
rpt_int = int(input("\nSegundos de captar el flujo "))
print("Reportes cada" ,rpt_int," segundos")
print("Control + c para salir")
f.write('Registro de litros gastados y temperatura promedio el dia: '+str(time.asctime(time.localtime(time.time()))))
bulb.turn_on()#encendemos el foco
bulb.set_hsv(360, 0, 1)
bulb.set_brightness(100)
bulb.set_color_temp(6500)
inicio = time.time()
while(rpt_int < 20):#rpt_int<10 or,,or GPIO.input(inpt)==True <-- esta linea para pruebas antes de todo lo demas
    rpt_int+=1
    TotLit = round(tot_cnt*constant,1)
    if(TotLit>=2 and aux==0):
        bulb.set_rgb(243 ,159, 24)
        bulb.set_brightness(100)
        bulb.set_color_temp(6500)#color rojo al foco
        print("Excediste de litros")
        aux = 1
    time.sleep(0.9)

final=time.time()
tiempo = round((final-inicio),2)
print('Litros gastados: ',TotLit)
print('Tiempo:  ',tiempo,' segundos')

f.write('\nLitros gastados: '+str(TotLit))
f.write('\nTiempo: '+str(tiempo))
f.flush()

GPIO.cleanup()
f.close()
bulb.turn_off()
print("Se acabo")
    
