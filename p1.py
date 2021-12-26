import RPi.GPIO as GPIO
import time, sys
f = open('flowmeter.txt','a')

GPIO.setmode(GPIO.BCM)
inpt = 13
led = 16
GPIO.setup(inpt,GPIO.IN)
GPIO.setup(led,GPIO.OUT)
minutos = 0
constant = 0.006
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
    
GPIO.add_event_detect(inpt,GPIO.FALLING,callback=Pulse_cnt,bouncetime=10)

#MAIN
print("Aproximacion de flujo de agua",str(time.asctime(time.localtime(time.time()))))
rpt_int = int(input("Segundos de captar el flujo "))
print("Reportes cada" ,rpt_int," segundos")
print("Control + c para salir")
f.write('\nFlujo de agua - Aproximado - Reportando cada '+str(rpt_int)+' segundos'+str(time.asctime(time.localtime(time.time()))))
inicio = time.time()
while(rpt_int < 10 or GPIO.input(inpt)==True):#rpt_int<10 or <-- esta linea para pruebas antes de todo lo demas
    rpt_int+=1
    time_new = time.time
    rate_cnt = 0
    minutos+=1
    LperM = round(((rate_cnt*constant)/(rpt_int/60)),2)
    TotLit = round(tot_cnt*constant,1)
    if(TotLit>=0.2 and aux==0):
        GPIO.output(led, GPIO.HIGH)
        print("Excediste de litros")
        aux = 1
    time.sleep(1)


final=time.time()
tiempo = round((final-inicio),2)
print('Litros totales ',TotLit)
print('Tiempo  ',tiempo)
#f.write('\n Litros/minutos'+str(LperM))
f.write(' Total de litros: '+str(TotLit))
f.write(' Tiempo '+str(tiempo))
f.flush()
if(GPIO.input(led)==True):
    GPIO.output(led,GPIO.LOW)

GPIO.cleanup()
f.close()
print("Se acabo")