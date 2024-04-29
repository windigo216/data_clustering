from utils import Vector
import random

def cluster_dist(self, other):
    min_dist = 1000
    for s in self.positions:
        for o in other.positions:
            min_dist = min(min_dist, (s-o).mag())
    return min_dist

class Cluster:
    def __init__(self, right, left):
        self.right = right
        self.left = left
        self.positions = right.positions + left.positions
    
class ClusterLeaf:
    def __init__(self, positions):
        self.positions = positions
    

def dendrogram(clusters):
    while len(clusters) != 1:
        min = [-1, -1, 1000]
        dist = 100
        # min is a list of the i, j, dist with minimum separation
        for i in range(len(clusters)):
            for j in range(i):
                dist = cluster_dist(clusters[i], clusters[j])
                if dist < min[2]:
                    min = [j, i, dist]
        new = Cluster(clusters[i], clusters[j])
        del clusters[i]
        del clusters[j]
        clusters.append(new)
    return clusters


def SLHAC(data_vectors):
    clusters = []
    for d in data_vectors:
        clusters+=[ClusterLeaf([d])]
    print(len(dendrogram(clusters)[0].positions))

vectors_around_0202 = [Vector([0.2 + random.uniform(-0.1, 0.1), 0.2 + random.uniform(-0.1, 0.1)]) for i in range(40)]
vectors_around_0508 = [Vector([0.5 + random.uniform(-0.1, 0.1), 0.8 + random.uniform(-0.1, 0.1)]) for i in range(40)]
vectors_around_0209 = [Vector([0.2 + random.uniform(-0.1, 0.1), 0.9 + random.uniform(-0.1, 0.1)]) for i in range(40)]
# vectors_around_0804 = [Vector([0.8 + random.uniform(-0.1, 0.1), 0.4 + random.uniform(-0.1, 0.1)]) for i in range(40)]
data = vectors_around_0202 + vectors_around_0508 + vectors_around_0209 

SLHAC(data)