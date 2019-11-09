import sys
import time
import zmq

context = zmq.Context()

# **Sink to Fan
SinkFan = context.socket(zmq.PUSH)
SinkFan.connect("tcp://localhost:5556")

# **Recibe todo
recibe = context.socket(zmq.PULL)
recibe.bind("tcp://*:5554")

TotalWorkers = 0
while True:
    s = recibe.recv_string()
    if s == '1':
        TotalWorkers += 1
    else:
        break
SinkFan.send_string(str(TotalWorkers))




