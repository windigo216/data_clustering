import math

class Vector:
    def __init__(self, nums):
        self.nums = nums
    
    def __add__(self, other):
        return Vector(list(map(lambda me, you: me + you, self.nums, other.nums)))
    
    def __sub__(self, other):
        return Vector(list(map(lambda me, you: me - you, self.nums, other.nums)))
    
    def __truediv__(self, scalar):
        return Vector(list(map(lambda e: e/scalar, self.nums)))
    
    def mag(self):
        sum = 0
        for num in self.nums:
            sum += num * num
        return math.sqrt(sum)
    
    def __eq__(self, other):
        return self.nums == other.nums