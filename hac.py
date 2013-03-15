
# import sys
# import random
from utils import *
import pylab as plt
import matplotlib as mpl

class Cluster:

    def __init__(self, points):
        self.points = points

    @staticmethod
    def merge_clusters(cluster1, cluster2):
        return Cluster(cluster1.points + cluster2.points)

class HAC:
    def __init__(self, data, k, fn):
        self.k = k
        self.clusters = map(lambda d: Cluster([d[:]]), data)
        self.distance_function = fn
        self.distances = {}

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
            print len(self.clusters)
            self.merge_closest_cluster()

        return self.clusters

    def print_table(self):

        plt.figure()
        col_labels=['col1','col2','col3']
        row_labels=['row1','row2','row3']
        table_vals=[[11,12,13],[21,22,23],[31,32,33]]

        # the rectangle is where I want to place the table
        the_table = plt.table(cellText=table_vals,
                          colWidths = [0.1]*3,
                          rowLabels=row_labels,
                          colLabels=col_labels,
                          loc='center right')
        plt.text(12,3.4,'Table Title',size=8)

        plt.show()

        '''
        mpl.rc('text', usetex=True)
        plt.figure()
        num_instances = map(lambda c: len(c.points), self.clusters)
        table = r"\begin{tabular}{ c } & Number of instances \\\hline"
        for i in range(len(self.clusters)):
            table += "Cluster {0} & {1} \\\hline".format(i, num_instances[i])
        table += "end{tabular}"
        plt.text(0,0,table,size=12)
        plt.show()
        '''
