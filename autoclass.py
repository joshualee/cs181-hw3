import random

def discrete_data(data):
  for datum in data:
    for i, value in enumerate(datum):
      datum[i] = 1.0 if value >= 0.5 else 0.0
  return data

def autoclass(data, K):
  data = discrete_data(data[:])
  N = float(len(data))
  D = len(data[0])
  
  # Initialize probabilities
  pi = [1.0/K] * K
  theta = [[random.uniform(0, 1) for d in range(D)] for k in range(K)]
  p = [0.0] * K
  p_x_n = [0.0] * K
  
  epsilon = 0.00001 # for convergence
  converged = False
  iterations = 0
  
  while not converged:
    iterations += 1
    print "iteration {0}".format(iterations)
    
    E_N = [0.0] * K
    E_N1 = [[0] * D for k in range(K)]
    
    for x_n in data:
      for k in range(K):
        p[k] = pi[k]
        for d in range(D):
          p[k] *= pow(theta[k][d], x_n[d]) * pow(1 - theta[k][d], 1 - x_n[d])
      
      for k in range(K):
        p_x_n[k] = p[k] / sum(p)
        E_N[k] += p_x_n[k]
      
      for d in range(D):
          if x_n[d] == 1:
            for k in range(K):
              E_N1[k][d] += p_x_n[k]
        
    # Maximization Step
    converged = True
    for k in range(K):
      old = pi[k]
      pi[k] = E_N[k] / N
      converged &= abs(old-pi[k]) <= epsilon
      for d in range(D):
        old = theta[k][d]
        theta[k][d] = E_N1[k][d] / E_N[k]
        converged &= abs(old-pi[k]) <= epsilon