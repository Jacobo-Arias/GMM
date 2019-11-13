import zmq
import numpy as np
from scipy.stats import multivariate_normal

context = zmq.Context()

# **Fan to worker
fan = context.socket(zmq.PULL)
fan.connect("tcp://localhost:5555")

# **Worker to sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5554")
pi,cov,mu = None,None,None
sink.send_string('1')
X = None
while True:
    datos = fan.recv_json()
    if 'datos' in datos:
        X = np.array(datos['datos'])
        reg_cov = 1e-6*np.identity(len(X[0]))
    pi = datos['pi']
    mu = datos['mu']
    cov = datos['cov']
    r_ic = np.zeros((len(X),len(cov)))
    for m,co,p,r in zip(mu,cov,pi,range(len(r_ic[0]))):
        # print(cov)
        # print()
        co+=reg_cov
        print(len(m))
        mn = multivariate_normal(mean=m,cov=co).pdf(X)
        r_ic[:,r] = p*mn/np.sum([pi_c*multivariate_normal(mean=mu_c,cov=cov_c).pdf(X) for pi_c,mu_c,cov_c in zip(pi,mu,cov+reg_cov)],axis=0)
        print(r_ic)
        input()
    X = np.ndarray.tolist(X)
    r_ic = np.ndarray.tolist(r_ic)
    datos = {
        'datos':X,
        'r_ic':r_ic
    }
