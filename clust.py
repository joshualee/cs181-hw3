# clust.py
# -------
# Joshua Lee and Sally

# for graphing
import matplotlib.pyplot as plt
from pylab import *

import sys
import random

# our code
import kmeans
from hac import *

DATAFILE = "adults-small.txt"

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

def graph(xaxis, yaxis, title="Title", xlabel="X Axis", ylabel="Y Axis"):
  plt.clf()
  plt.plot(xaxis, yaxis)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  savefig(title + ".pdf") # save the figure to a file
  plt.show() # show the figure

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

    # ==================== #
    # Our Code Start       #
    # ==================== #

    # kmeans_performances = []
    # kmeans_range = range(2, 11)
    # for k in kmeans_range:
      # prototypes, performance = kmeans.kmeans(k, data[:1000])
      # kmeans_performances.append(performance)

    # graph(kmeans_range, kmeans_performances,
      # title="K-Means Performance",
      # xlabel="K",
      # ylabel="Mean Squared Error"
    # )

    min_hac = HAC(data[:100], 4, cmin)
    min_hac.hac()
    min_hac.print_table()

    max_hac = HAC(data[:100], 4, cmax)
    max_hac.hac()
    max_hac.print_table()

if __name__ == "__main__":
    validateInput()
    main()
