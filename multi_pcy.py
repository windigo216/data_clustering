import hashlib
import csv
import collections
import itertools
import math

"""Read in the CSV data
"""
data = list(csv.DictReader(open("gpp.csv")))

"""Constants relating to the size of the data
"""
data_size = len(data)+1
data_width = len(data[0])
threshold = 0.02 * data_size

def hash_bounded(x):
    """Hash two numbers to a value between 0 and data_size - 1

    Args:
        x (list(int)): A key of an item

    Returns:
        int: The hash
    """
    concat = ("0".join(list(map(str, sorted(x))))).encode()
    hash_hex = hashlib.sha256(concat).hexdigest()[:8]
    hash_dec = int(hash_hex, 16)

    return hash_dec % int(data_size/5)
    # return hash_dec % 10

"""Functions for manipulating the hashable representation of collections of items
"""
def stringify(x):
    return "||".join(list(map(str, sorted(x))))

def unstringify(x):
    return list(map(int, x.split("||")))

def unstrlistify(x, base_items_to_ints):
    return list(map(lambda a: base_items_to_ints[a], x.split("||")))

def strunlistify(x):
    return x.split("||")

def pcy(test_items, base_items_to_ints, base_ints_to_items):
    # test_items is the set of items which passed the previous stage.
    # Initialize with the list of all elements originally
    """Do the PCY algorithm

    Args:
        test_items (List(List(int))): The set of collections that passed the previous PCY test or the original list of all items
        base_items_to_ints (Dict): Mapping of str to int
        base_ints_to_items (Dict): Mapping of int to str

    Returns:
        The frequent sets of length 1 higher than those inputted
    """
    items_to_ints = {}
    ints_to_items = {}
    for i in range(len(test_items)):
        ints_to_items[i] = stringify(test_items[i])
        items_to_ints[stringify(test_items[i])] = i

    new_item_size = len(test_items[0]) + 1
    collection_hashmap = collections.Counter([])
    item_frequency = collections.Counter([])

    count = 0
    print(len(test_items))
    for i in range(data_size-1):
        values = list(set(data[i].values()))
        try:
            values.remove("")
        except:
            pass
        count += math.comb(len(values), 2)
        for item in test_items:
            if set(item).issubset(set(values)):
                item_frequency.update([stringify(item)])
        permuted = set(itertools.combinations(list(map(lambda x: base_items_to_ints[x], values)), new_item_size))
        for_collection = list(map(hash_bounded, list(map(sorted, permuted))))
        collection_hashmap.update(for_collection)
    frequent_buckets = [x for x in collection_hashmap.keys() if collection_hashmap[x] > threshold]
    frequent_items = list(map(lambda x: items_to_ints[x], [x for x in item_frequency.keys() if item_frequency[x] > threshold]))
    potentially_frequent = []
    for i in range(len(frequent_items)):
        for j in range(i):
            a = unstrlistify(ints_to_items[frequent_items[i]], base_items_to_ints)
            b = unstrlistify(ints_to_items[frequent_items[j]], base_items_to_ints)
            combination = list(set(a + b))
            if len(combination) != new_item_size:
                continue
            elif hash_bounded(combination) in frequent_buckets:
                potentially_frequent.append(combination)
    collection_counter = collections.Counter([])
    for i in range(data_size - 1):
        values = list(set(data[i].values()))
        try:
            values.remove("")
        except:
            pass
        for p in potentially_frequent:
            if set(p).issubset(list(map(lambda x: base_items_to_ints[x], set(values)))):
                collection_counter.update([stringify(p)])
    frequent = []
    for k in collection_counter.keys():
        if collection_counter[k] > threshold:
            frequent.append(list(map(lambda x: base_ints_to_items[x], unstringify(k))))
    for i in range(len(frequent)):
        frequent[i] = list(set(itertools.chain.from_iterable(map(lambda e: strunlistify(e), frequent[i]))))
    print("frequent:", frequent)
    return frequent


def pcy_wrapper():
    """Computes PCY three times (gets frequent pairs, triples, and quadruples)
    """
    val_counts = collections.Counter([])
    for basket in data:
        x = list(set(basket.values()))
        try:
            x.remove("")
        except:
            pass
        val_counts.update(x)
    vals = list(map(lambda x: [x], list(val_counts.keys())))
    base_items_to_ints = {}
    base_ints_to_items = {}
    for i in range(len(vals)):
        base_ints_to_items[i] = stringify(vals[i])
        base_items_to_ints[stringify(vals[i])] = i

    res1 = pcy(vals, base_items_to_ints, base_ints_to_items)
    res2 = pcy(res1, base_items_to_ints, base_ints_to_items)
    res3 = pcy(res2, base_items_to_ints, base_ints_to_items)

    with open("pcy_doubles.txt", "w") as pcy2:
        pcy2.writelines(resToWritable(res1))
    
    with open("pcy_triples.txt", "w") as pcy3:
        pcy3.writelines(resToWritable(res2))
    
    with open("pcy_quadruples.txt", "w") as pcy4:
        pcy4.writelines(resToWritable(res3))

def resToWritable(res):
    return map(lambda x: ", ".join(x) + "\n", res)

pcy_wrapper()