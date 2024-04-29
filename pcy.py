import hashlib
import csv
import collections
import math

"""Read in the CSV data
"""
data = list(csv.DictReader(open("test.csv")))

"""Initialize the hashmaps and counters
"""
items_to_ints = {} 
pair_hashmap = collections.Counter([])
item_frequency = collections.Counter([])
double_freq_counter =  collections.Counter([])

"""Constants relating to the size of the data
"""
data_size = len(data)+1
data_width = len(data[0])
threshold = 0.01 * data_size

def hash(k1, k2):
    """Hash two numbers to a value between 0 and data_size - 1

    Args:
        k1 (int): A key of an item
        k2 (int): Another key of an item

    Returns:
        int: The hash
    """
    concat = (str(k1) + str(k2)).encode()
    hash_hex = hashlib.sha256(concat).hexdigest()[:8]
    hash_dec = int(hash_hex, 16)
    return hash_dec % int(data_size/5)

def pcy_first_pass():
    """Does the first step of PCY

    Returns:
        list(list(int)): The candidate pairs
    """
    for i in range(data_size - 1):
        basket = []
        for item in data[i].values():
            if str(item) != "":
                if item not in items_to_ints.keys():
                    items_to_ints[item] = len(items_to_ints.values())
                    item_frequency[item] = 1
                    basket.append(len(items_to_ints.values()) - 1)
                else:
                    item_frequency[item] += 1
                    basket.append(items_to_ints[item])
        for i in range(len(basket)):
            for j in range(i):
                hashed = hash(j, i)
                if hashed in pair_hashmap.keys():
                    pair_hashmap[hashed] += 1
                else:
                    pair_hashmap[hashed] = 1
    potentially_frequent = []
    key_bitmap = {}
    for k in pair_hashmap.keys():
        if pair_hashmap[k] > threshold:
            key_bitmap[k] = 1
        else:
            key_bitmap[k] = 0
    for i in items_to_ints.values():
        for j in range(i):
            try:
                key = key_bitmap[hash(j, i)]
            except:
                continue
            if key == 1:
                potentially_frequent.append([i, j])
    return potentially_frequent

def pcy_second_pass():
    """Does the second step of PCY

    Returns:
        list(list(int)): The frequent pairs
    """
    potentially_frequent = pcy_first_pass()
    for p in potentially_frequent:
        double_freq_counter[str(p[0]) + "||" + str(p[1])] = 0
    for i in range(data_size-1):
        basket = []
        for item in data[i].values():
            if str(item) != "":
                    basket.append(items_to_ints[item])
        for p in potentially_frequent:
            if p[0] in basket and p[1] in basket:
                double_freq_counter[str(p[0]) + "||" + str(p[1])] += 1
    frequent = []
    for k in double_freq_counter.keys():
        if double_freq_counter[k] > threshold:
            [i1, i2] = list(map(int, k.split("||")))
            frequent_pair = [i1, i2]
            frequent.append(frequent_pair)
    return frequent
            
def get_pcy_analysis():
    """Uses the frequent pairs to generate a txt file containing a summary of them
    """
    frequent_pairs = pcy_second_pass()
    keys = list(items_to_ints.keys())
    with open('pcy_out.txt', 'w') as out:
        for [i1, i2] in frequent_pairs:
            i1name = keys[i1]
            i2name = keys[i2]
            double_freq = double_freq_counter[str(i1) + "||" + str(i2)]
            out.write(i1name +  ", " + i2name + "\n")
            out.write(i2name + " association with " + i1name + " = " + str(double_freq/item_frequency[keys[i2]]) + "\n")
            out.write(i1name + " association with " + i2name + " = " + str(double_freq/item_frequency[keys[i1]]) + "\n")

def test():
    count = 0
    for line in data:
        line = list(set(line))
        try:
            line.remove("")
        except:
            pass
        print(len(line))
        count += math.comb(len(line), 2)
    print(count)
    print(len(data))

# get_pcy_analysis()
test()