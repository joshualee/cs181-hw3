
# import sys
# import random
from utils import *
import pylab as plt
import matplotlib as mpl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class Cluster:

    def __init__(self, points):
        self.points = points

    @staticmethod
    def merge_clusters(cluster1, cluster2):
        return Cluster(cluster1.points + cluster2.points)

class HAC:
    def __init__(self, data, k, fn, name="HAC Cluster"):
        self.k = k
        self.clusters = map(lambda d: Cluster([d[:]]), data)
        self.distance_function = fn
        self.distances = {}
        self.name = name

    def merge_closest_cluster(self):
        '''
            For each pair of clusters check first whether we know the distance
            between these clusters. If we do not, calculate the distance and
            add it to self.distances. Check to see if we have a new low
            distance. If so, then make this pair of clusters our best pair.
            After we've found the absolute best pair. Merge them and delete
            the old clusters
        '''
        best_distance = float("infinity")
        best_pair = (None, None)

        for index, cluster1 in enumerate(self.clusters):
            for cluster2 in self.clusters[index+1::]:

                if (cluster1, cluster2) in self.distances:
                    distance = self.distances[(cluster1, cluster2)]
                else:
                    distance = self.distance_function(cluster1.points, cluster2.points, squareDistance)
                    self.distances[(cluster1, cluster2)] = distance

                if distance < best_distance:
                    best_distance = distance
                    best_pair = (cluster1, cluster2)

        del self.distances[best_pair]
        new_cluster = Cluster.merge_clusters(*best_pair)
        self.clusters.append(new_cluster)
        self.clusters.remove(best_pair[0])
        self.clusters.remove(best_pair[1])

    def hac(self):
        while len(self.clusters) > self.k:
            self.merge_closest_cluster()

    def print_table(self, display=False):
        title = "HAC Table | " + self.name
        plt.figure()
        
        cells = map(lambda c: [len(c.points)], self.clusters)
        rows = map(lambda i: "Cluster {0}".format(i), range(1, len(self.clusters)+1))
        the_table = plt.table(
          cellText=cells,
          colWidths=[0.2],
          rowLabels=rows,
          colLabels=["# Instances"],
          loc="center"
        )
        
        plt.text(0, 0, title, size=20)
        
        plt.savefig(title + ".pdf")
        if display: plt.show()

    def scatter_plot(self, display=False):
      title = "HAC Scatter Plot | " + self.name
      
      colors = ["#5AA2E0", "#EB4949", "#49EB61", "#ECF238"]
      fig = mpl.pyplot.figure()
      ax = fig.add_subplot(111, projection='3d')
      for i, c in enumerate(self.clusters):
        xs = map(lambda p: p[0], c.points)
        ys = map(lambda p: p[1], c.points)
        zs = map(lambda p: p[2], c.points)
        ax.scatter(xs, ys, zs, c=colors[i])

      mpl.pyplot.title(title)
      ax.set_xlabel('X')
      ax.set_ylabel('Y')
      ax.set_zlabel('Z')
      plt.savefig(title + ".pdf")
      
      if display: mpl.pyplot.show()
