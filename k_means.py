import math
import functools
import random
from utils import Vector
import matplotlib.pyplot as plt
import copy
    
class Mean:
    def __init__(self, position, responsibility):
        self.position = position
        self.responsibility = responsibility
    
    def __eq__(self, other):
        return self.position == other.position and self.responsibility == other.responsibility

def centroid(vectors, vector_size):
    if len(vectors) == 0:
        return Vector([random.uniform(0, 1) for i in range(vector_size)])
    return functools.reduce(lambda a, b: a + b, vectors)/len(vectors)
    

def k_means_initialization(data_vectors, k):
    centroids = []
    data_size = len(data_vectors)
    centroids.append(Mean(random.sample(data_vectors, 1)[0], []))
    for i in range(k-1):
        dists = []
        for d in data_vectors:
            minDist = 10
            for c in centroids:
                diff = (c.position - d).mag()
                if diff < minDist and diff > 0:
                    minDist = diff
            dists.append(minDist)
        dists = list(map(lambda x: x**2, dists))
        centroid_indicator = random.uniform(0, sum(dists))
        sum_so_far = 0
        key = 0
        for i in range(data_size):
            sum_so_far += dists[i]
            if sum_so_far > centroid_indicator:
                key = 1
                centroids.append(Mean(data_vectors[i], []))
                break
        if key != 1:
            print(dists, centroid_indicator)
    for c in centroids:
        print(c.position.nums)
        if c.position not in data_vectors:
            print("oh no")
    return centroids

def k_means(data_vectors, k, centroids=None):
    # make data_vectors havs vals bounded to [0, 1]. Scale as necessary
    data_size = len(data_vectors)
    data_dimensions = len(data_vectors[0].nums)
    if not centroids:
        centroids = [Mean(Vector([random.uniform(0, 1) for i in range(data_dimensions)]), []) for j in range(k)]
    last_centroids = [None]
    count = 0
    for i in range(10):
        count += 1
        for v in range(data_size):
            closest = [0, 2]
            for i in range(k):
                dist = (centroids[i].position - data_vectors[v]).mag()
                if dist < closest[1]:
                    closest = [i, dist]
            centroids[closest[0]].responsibility.append(data_vectors[v])

        key = 0
        
        if last_centroids[-1] != None:
            for [a, b] in zip(last_centroids[-1], centroids):
                if a.position.nums != b.position.nums:
                    last_centroids.append(copy.deepcopy(centroids))
                    key = 1
            if key == 0:
                break
        
        else:
            last_centroids.append(copy.deepcopy(centroids))
        plot = plt.figure(count)
        for c in centroids:
            vector_vals = list(map(lambda vector: vector.nums, c.responsibility))
            plt.scatter(list(map(lambda x: x[0], vector_vals)), list(map(lambda x: x[1], vector_vals)))
            centroid_x = []
            centroid_y = []
        for c in centroids:
            centroid_x.append(c.position.nums[0])
            centroid_y.append(c.position.nums[1])
        plt.scatter(centroid_x, centroid_y)

        plt.show()

        for c in centroids:
            c.position = centroid(c.responsibility, data_dimensions)
            c.responsibility = []
    return centroids

def k_means_total(data_vectors, k):
    centroids=k_means_initialization(data_vectors, k)
    return k_means(data_vectors, k, centroids=centroids)

def inertia(centroids):
    sum = 0
    for c in centroids:
        for v in c.responsibility:
            sum += (c.position - v).mag()
    return sum

def k_means_test():
    d = [Vector([0.5 + random.uniform(0, 0.1), 0.5 + random.uniform(0, 0.1)]) for i in range(20)] 
    d1 = []
    for i in range(100):
        angle = random.uniform(0, math.pi * 2)
        r = random.uniform(0.4, 0.5)
        d1.append(Vector([0.5 + r * math.cos(angle), 0.5 + r * math.sin(angle)]))
    d += d1

    vectors_around_0202 = [Vector([0.2 + random.uniform(-0.1, 0.1), 0.2 + random.uniform(-0.1, 0.1)]) for i in range(40)]
    vectors_around_0508 = [Vector([0.5 + random.uniform(-0.1, 0.1), 0.8 + random.uniform(-0.1, 0.1)]) for i in range(40)]
    vectors_around_0209 = [Vector([0.2 + random.uniform(-0.1, 0.1), 0.9 + random.uniform(-0.1, 0.1)]) for i in range(40)]

    data = vectors_around_0202 + vectors_around_0508 + vectors_around_0209 


    # k_means(data, 3, centroids=k_means_initialization(data, 3))
    # x = []
    # y = []
    # plots = []
    # for i in range(1, 6):
    #     x.append(i)
    #     centroids = k_means_total(data, i)
    #     y.append(inertia(centroids))
    #     plot = plt.figure(i)
    #     # if i == 4:
    #     for c in centroids:
    #         vector_vals = list(map(lambda vector: vector.nums, c.responsibility))
    #         # print(list(map(lambda x: x[0], vector_vals)), " and ", list(map(lambda x: x[1], vector_vals)))
    #         # print(len(list(map(lambda x: x[0], vector_vals))), " and ", len(list(map(lambda x: x[1], vector_vals))))
    #         # print(list(map(lambda x: x[0], vector_vals)))
    #         plt.scatter(list(map(lambda x: x[0], vector_vals)), list(map(lambda x: x[1], vector_vals)))
    #         centroid_x = []
    #         centroid_y = []
    #     for c in centroids:
    #         centroid_x.append(c.position.nums[0])
    #         centroid_y.append(c.position.nums[1])
    #     plt.scatter(centroid_x, centroid_y)


    centroids = k_means_total(data, 3)
    ine = inertia(centroids)


    # print(inertia(k_means_total(data, i)))

    plt.show()

k_means_test()