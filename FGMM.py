import zmq
import random
import json
import time

#TODO Street||Month||Year||Boundaries - ZIP Codes||Community Areas||Zip Codes||Wards||Computed Region

# xls = pd.read_csv('datos.csv',na_values=['no info','.']#,index_col='Month'
#                     )

# xls.head(#)
# meses= xls['Month']
# print(xls)

with open('datos.json') as json_file:
    data = json.load(json_file)
    for i in data:
        print (i)

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
n = input()
print('start')
Tosink.send_string('start')
TotalWorkers = SinkFan.recv_string()
TotalWorkers = int(TotalWorkers)

MatrizCov=[]
VectorU=[]
for i in range(len(data[0])):
    MatrizCov.append([])
    VectorU.append(random.random()) #random.uniform(a,b)  a<=N<=b || b<=N<=a
    for j in range(len(data)):
        MatrizCov[i].append(random.random())




while True:
    sobrante = len(data)%TotalWorkers
    Lendatos = int((len(data)-sobrante)/(TotalWorkers))
    cont = 0
    for i in range(TotalWorkers):
        if sobrante>0:
            añadir=[data.pop(-1)]
        ToSend = {
            'Datos':data[cont*Lendatos:(cont+1)*Lendatos]+añadir,
            'Vector':[],
            'Matriz':[[]]
        }
        Mandar.send_json(ToSend)
        añadir=[]
    RecivSink = SinkFan.recv_json()
