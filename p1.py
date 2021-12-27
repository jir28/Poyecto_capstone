
import RPi.GPIO as GPIO #puertos de raspberry
import time
#from w1thermsensor import W1ThermSensor #libreria para sensor de temperatura de agua
from yeelight import Bulb#Librerias para foco MI
from yeelight import LightType

f = open('flowmeter.txt','a')

GPIO.setmode(GPIO.BCM)
inpt = 13
led = 16
GPIO.setup(inpt,GPIO.IN)
GPIO.setup(led,GPIO.OUT)
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
inicio = time.time()
while(rpt_int < 20):#rpt_int<10 or,,or GPIO.input(inpt)==True <-- esta linea para pruebas antes de todo lo demas
    rpt_int+=1
    TotLit = round(tot_cnt*constant,1)
    if(TotLit>=1 and aux==0):
        GPIO.output(led, GPIO.HIGH)
        print("Excediste de litros")
        aux = 1
    time.sleep(1)


final=time.time()
tiempo = round((final-inicio),2)
print('Litros gastados: ',TotLit)
print('Tiempo:  ',tiempo,' segundos')

f.write('\nLitros gastados: '+str(TotLit))
f.write('\nTiempo: '+str(tiempo))
f.flush()

if(GPIO.input(led)==True):
    GPIO.output(led,GPIO.LOW)

GPIO.cleanup()
f.close()
print("Se acabo")
    
