import random
import math
from math import log
from clust import graph
import time

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
  
  epsilon = 0.00001 # for convergence
  converged = False
  iterations = 0
  likelihood = 0
  likelihoods = []
  
  while not converged:
    # Expectatoin Step
    E_N = [0.0] * K
    E_N1 = [[0] * D for k in range(K)]
    
    for x_n in data:
      p = [0.0] * K
      p_x_n = [0.0] * K
      
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
    for k in range(K):
      old = pi[k]
      pi[k] = E_N[k] / N
      # assert(pi[k] != 0)
      # print old, pi[k]
      # converged &= (abs(old-pi[k]) <= epsilon)
      for d in range(D):
        old = theta[k][d]
        theta[k][d] = E_N1[k][d] / E_N[k]
        # print old, theta[k][d]
        # converged &= (abs(old-pi[k]) <= epsilon)
    
    iterations += 1
    old_likelihood = likelihood
    likelihood = log_likelihood(data, pi, theta, K, D)
    likelihoods.append(likelihood)
    converged = abs(old_likelihood - likelihood) <= epsilon
    # print "{0}: {1}".format(iterations, likelihood)
  
  # graph(range(iterations), likelihoods, title="Autoclass Likelihood", xlabel="Iterations", ylabel="Likelihood", display=False)
  return likelihood

def extra_credit(data):
  autoclass_range = range(2, 11)
  likelihoods = []
  run_times = []
  for k in autoclass_range:
    start_time = time.time()
    likelihoods.append(autoclass(data, k))
    end_time = time.time()
    run_time = end_time - start_time
    print "Run time: {0} secs".format(run_time)
    run_times.append(run_time)
  print run_times
  graph(autoclass_range, run_times, title="Autoclass Run Time For Varying K", xlabel="K", ylabel="Run-time (s)", display=False)
  # graph(autoclass_range, likelihoods, title="Autoclass Max Likelihood For Varying K", xlabel="K", ylabel="Maximum Likelihood", display=False)

def log_likelihood(data, pi, theta, K, D):
  likelihood = 0.0
  for x_n in data:
    outer_sum = 0.0
    for k in range(K):
      inner_sum = 0.0
      for d in range(D):
        try:
          if x_n[d] == 1:
            inner_sum += log(theta[k][d])
          else:
            inner_sum += log(1-theta[k][d])
        except ValueError:
          inner_sum += float("-inf")
      outer_sum += pow(math.e, log(pi[k]) + inner_sum)
    likelihood += log(outer_sum)
  return likelihood