# clust.py
# -------
# YOUR NAME HERE

import sys
import random
from utils import *

class Data:
  def __init__(self, value, prototype=None):
    self.value = value
    self.prototype = prototype
  
  @staticmethod
  def generate_from_data(data):
    return map(lambda d: Data(d[:]), data)

class Prototype:
  def __init__(self, value, data=[]):
    self.value = value
    self.data = data
  
  @staticmethod
  def random_from_data(k, data):
    sample_data = random.sample(data, k)
    return map(lambda d: Prototype(d[:]), sample_data)

def kmeans(k, data):
  prototypes = Prototype.random_from_data(k, data)
  data = Data.generate_from_data(data)
  
  converged = False
  epsilon = 0.0 # convergence criterion
  iterations = 0  
  while not converged:
    # ---
    # 1. update responsibility to nearest prototype
    # ---
  
    # clear prototypes data list
    for p in prototypes:
      p.data = []
  
    for d in data:
      # set data to point to correct prototype
      d.prototype = argmin(prototypes, lambda p: squareDistance(d.value, p.value))
    
      # add data to prototype's list
      d.prototype.data.append(d)
    
    # ---
    # 2. update prototypes based on data associated with it
    # ---  
    converged = True
    for p in prototypes:
      before = p.value[:]
      data_values = map(lambda d: d.value, p.data)
      p.value = map(lambda x: x/len(p.data), [sum(a) for a in zip(*data_values)])
      for old, new in zip(before, p.value):
        converged &= (abs(new-old) <= epsilon)

  return (prototypes, performance(data))

def performance(data):
  return reduce(lambda s, d: s + squareDistance(d.value, d.prototype.value), data, 0.0) / len(data)
  
  