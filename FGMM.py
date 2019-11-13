import zmq
import random
import json
import time
import numpy as np

#TODO Street||Month||Year||Boundaries - ZIP Codes||Community Areas||Zip Codes||Wards||Computed Region
#TODO --238-||-12--||--2-||---------61-----------||-----77--------||----70---||-50--||----53---------


Nclusters = int(input("Cuantos grupos?: "))

with open('datos.json') as json_file:
    datos = json.load(json_file)
    for i in datos:
        i.pop(5)
    data = np.array(datos)


context = zmq.Context()

# **Manda todo
Mandar = context.socket(zmq.PUSH)
Mandar.bind("tcp://*:5555")

# **Sink to Fan
SinkFan = context.socket(zmq.PULL)
SinkFan.bind("tcp://*:5556")


Tosink = context.socket(zmq.PUSH)
Tosink.connect("tcp://localhost:5554")

print("Press enter when workers are ready...")
input()
print('start')
Tosink.send_string('start')

mu = []
for j in range(Nclusters):
    mu.append([])
    for i in range(len(datos[0])):
        mu[j].append(random.uniform(min(data[:,0]),max(data[:,0])))


cov=[]
for k in range(Nclusters):
    cov.append([])
    for i in range(len(datos[0])):
        cov[k].append([])
        for j in range(len(datos[0])):
            if j == i:
                a = 1
            else:
                a=0
            cov[k][i].append(a)

pii = [1/Nclusters for i in range(Nclusters)]

TotalWorkers = SinkFan.recv_string()
TotalWorkers = int(TotalWorkers)
sobrante = len(data)%TotalWorkers
Lendatos = int((len(data)-sobrante)/(TotalWorkers))
cont = 0
for i in range(TotalWorkers):
    if sobrante>0:
        añadir=[datos.pop(-1)]
    ToSend = {
        'datos':datos[cont*Lendatos:(cont+1)*Lendatos]+añadir,
        'mu':mu,
        'cov':cov,
        'pi':pii
    }
    Mandar.send_json(ToSend)
    añadir=[]
while True:
    RecivSink = SinkFan.recv_json()
    for i in range(TotalWorkers):
        Mandar.send_json(RecivSink)


