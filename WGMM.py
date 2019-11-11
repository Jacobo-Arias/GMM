import zmq

context = zmq.Context()

# **Fan to worker
fan = context.socket(zmq.PULL)
fan.connect("tcp://localhost:5555")

# **Worker to sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5554")

sink.send_string('1')

while True:
    datos = fan.recv_json()
