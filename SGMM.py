import zmq
import numpy as np
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
        print('Worker connected, total:' ,TotalWorkers)
    else:
        break
SinkFan.send_string(str(TotalWorkers))
X=np.array([1,2])
r_ic=np.array([1,2])
while True:
    for i in range(TotalWorkers):
        datos = recibe.recv_json()
        print(datos['datos'])
        X = np.array([X.flatten(),np.array(datos['datos']).flatten()])
        r_ic = np.array([r_ic.flatten(),np.array(datos['r_ic']).flatten()])
    X = X[1:]
    r_ic = r_ic[1:]
    mu = []
    cov = []
    pi = []
    for c in range(len(r_ic[0])):
        m_c = np.sum(r_ic[:,c],axis=0)
        mu_c = (1/m_c)*np.sum(X*r_ic[:,c].reshape(len(X),1),axis=0)
        mu.append(mu_c)
        cov.append(((1/m_c)*np.dot((np.array(r_ic[:,c]).reshape(len(X),1)*(X-mu_c)).T,(X-mu_c)))+reg_cov)
        pi.append(m_c/np.sum(r_ic))

    mu = np.ndarray.tolist(mu)
    cov = np.ndarray.tolist(cov)
    pi = np.ndarray.tolist(pi)
    enviar = {
        'mu' : mu,
        'cov' : cov,
        'pi' : pi
    }
    SinkFan.send_json(enviar)
    





