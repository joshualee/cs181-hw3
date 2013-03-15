import random

def discrete_data(data):
  for datum in data:
    for i, value in enumerate(datum):
      datum[i] = 1 if value >= 0.5 else 0
  return data

def autoclass(data):
  data = discrete_data(data[:])
  dimensions = len(data[0])
  N = len(data)
  
  # Initialize probabilities
  t_c = random.uniform(0, 1)
  t_1 = [1.0/dimensions] * dimensions
  t_0 = [1.0/dimensions] * dimensions
  
  epsilon = 0.00001 # for convergence
  converged = False
  iterations = 0
  
  while not converged:
    iterations += 1
    print "iteration {0}".format(iterations)
    
    e_n1 = 0.0
    e_d1 = [0.0] * dimensions
    e_d0 = [0.0] * dimensions
    
    for i, x_n in enumerate(data):
      p_1 = t_c
      p_0 = (1 - t_c)
      for d in range(dimensions):
        p_1 *= pow(t_1[d], x_n[d]) * pow(1 - t_1[d], 1 - x_n[d])
        p_0 *= pow(t_0[d], x_n[d]) * pow(1 - t_0[d], 1 - x_n[d])
        
      p_x_n = p_1 / (p_1 + p_0)
      e_n1 += p_x_n
      
      for d in range(dimensions):
        if x_n[d] == 1:
          e_d1[d] = p_x_n
          e_d0[d] = (1 - p_x_n)
      
    # Maximization Step
    old_t_c = t_c
    t_c = e_n1 / N
    
    converged = abs(old_t_c - t_c) <= epsilon
    for d in range(dimensions):
      t_1[d] = e_d1[d] / e_n1
      t_0[d] = e_d0[d] / (N - e_n1)