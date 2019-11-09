import zmq
import random
import time

#TODO Street||Month||Year||Boundaries - ZIP Codes||Community Areas||Zip Codes||Wards||Computed Region

# xls = pd.read_csv('datos.csv',na_values=['no info','.']#,index_col='Month'
#                     )

# xls.head(#)
# meses= xls['Month']
# print(xls)


# with open('datos.json') as json_file:
#     data = json.load(json_file)
#     for i in data:
#         print (i)



context = zmq.Context()

# **Manda todo
Mandar = context.socket(zmq.PUSH)
Mandar.bind("tcp://*:5555")

# **Sink to Fan
SinkFan = context.socket(zmq.PULL)
SinkFan.connect("tcp://localhost:5556")


Tosink = context.socket(zmq.PUSH)
Tosink.connect("tcp://localhost:5554")

print("Press enter when workers are ready...")
n = input()
print('start')
Tosink.send_string('start')
TotalWorkers = SinkFan.recv_string()
TotalWorkers = int(TotalWorkers)
print(TotalWorkers)


# Mandar.send_string(cadena)
# for i in range(int(n)):
#     workers.send_string(cadena)

# print("Work sent")
# while True:
#     pass
