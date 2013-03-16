# clust.py
# -------
# Joshua Lee and Sally

# for graphing
import matplotlib.pyplot as plt
from pylab import *
from scipy.stats import beta
import numpy as np

# python library
import sys
import random
import time

# our code
import kmeans
from hac import *
import autoclass

DATAFILE = "adults.txt"

#validateInput()

def validateInput():
    if len(sys.argv) != 3:
        return False
    if sys.argv[1] <= 0:
        return False
    if sys.argv[2] <= 0:
        return False
    return True


#-----------


def parseInput(datafile):
    """
    params datafile: a file object, as obtained from function `open`
    returns: a list of lists

    example (typical use):
    fin = open('myfile.txt')
    data = parseInput(fin)
    fin.close()
    """
    data = []
    for line in datafile:
        instance = line.split(",")
        instance = instance[:-1]
        data.append(map(lambda x:float(x),instance))
    return data


def printOutput(data, numExamples):
    for instance in data[:numExamples]:
        print ','.join([str(x) for x in instance])

def graph(xaxis, yaxis, title="Title", xlabel="X Axis", ylabel="Y Axis", display=False):
  plt.clf()
  plt.plot(xaxis, yaxis)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  savefig(title + ".pdf") # save the figure to a file
  if display: plt.show() # show the figure

def do_beta(display=False):
  a, b = 1, 1
  rv = beta(a, b)
  x = np.linspace(0, np.minimum(rv.dist.b, 3))
  h = plt.plot(x, rv.pdf(x))
  title = "Beta({0}, {1}) PDF".format(a, b)
  plt.title(title)
  savefig(title + ".pdf")
  if display: plt.show()

def do_kmeans(data, display=False):
  kmeans_performances = []
  kmeans_run_times = []
  kmeans_range = range(2, 11)
  for k in kmeans_range:
    start_time = time.time()
    prototypes, performance = kmeans.kmeans(k, data[:1000])
    end_time = time.time()
    run_time = end_time - start_time
    kmeans_run_times.append(run_time)
    # print "Run time {0}: {1} secs".format(k, run_time)
    kmeans_performances.append(performance)
    
  graph(kmeans_range, kmeans_performances,
    title="K-Means Performance",
    xlabel="K",
    ylabel="Mean Squared Error",
    display=display
  )
  
  # print kmeans_run_times
  # graph(kmeans_range, kmeans_run_times,
  #   title="K-Means Run Time",
  #   xlabel="K",
  #   ylabel="Run-time (s)",
  #   display=display
  # )

def do_hac(data):
  min_hac = HAC(data[:100], 4, cmin, name="Min")
  min_hac.hac()
  min_hac.print_table()
  min_hac.scatter_plot()

  max_hac = HAC(data[:100], 4, cmax, name="Max")
  max_hac.hac()
  max_hac.print_table()
  max_hac.scatter_plot()
    
  mean_hac = HAC(data[:200], 4, cmean, name="Mean")
  mean_hac.hac()
  mean_hac.print_table()
  mean_hac.scatter_plot()
    
  cent_hac = HAC(data[:200], 4, ccent, name="Centroid")
  cent_hac.hac()
  cent_hac.print_table()
  cent_hac.scatter_plot()

def do_autoclass(data):
  autoclass.autoclass(data[:1000], 4)
  # autoclass.extra_credit(data[:1000])

# main
# ----
# The main program loop
# You should modify this function to run your experiments

def main():
    # Validate the inputs
    if(validateInput() == False):
        print "Usage: clust numClusters numExamples"
        sys.exit(1);

    numClusters = int(sys.argv[1])
    numExamples = int(sys.argv[2])

    #Initialize the random seed

    random.seed()

    #Initialize the data

    dataset = file(DATAFILE, "r")
    if dataset == None:
        print "Unable to open data file"

    data = parseInput(dataset)

    dataset.close()
    printOutput(data,numExamples)
    
    # ---
    # K-Means
    # ---
    
    do_kmeans(data)
    
    # ---
    # HAC
    # ---

    do_hac(data)
    
    # ---
    # Autoclass
    # ---

    do_autoclass(data)
    
    # do_beta()

if __name__ == "__main__":
    validateInput()
    main()
