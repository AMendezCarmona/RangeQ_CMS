
import math
import numpy as np
import mmh3


def dyadic_interval(x,y):
    '''
    Obtain the left and right values of a Dyadic Range,
    following the next formula:

        Dx,y = [((x - 1) * 2) ^ y  + 1, (x * 2) ^ y]

    The function recieves the two parameters x and y.

    An example of use:

        from rangeqcms import dyadic_interval
        dyadic_interval(1,4)    # returns (1,16)
        dyadic_interval(2.5)    # returns (33,64)

    '''
    return (x - 1) * 2 ** y + 1, x * 2 ** y




class CountMinSketch:
    '''
    A class for probabilistic data structure Count-Min Sketch,
    intended for storing a sublinear approximation of a given set.
    This data structure becomes useful when it is difficult (or even impossible)
    to store the original set in local memory.

    This class has two parameters:

        - epsilon: factor of estimation error, [0,1]
        - delta: probability of obtaining and error within a factor of epsilon, [0,1]
    
    Using these two parameters, a zero matrix of size M x P is generated, where:

        - M = ln(1/delta)
        - P = e/epsilon

    For a detailed description of the data structure, see (Cormode, et al., 2005)
    '''
    def __init__(self, epsilon, delta):
        self.p = math.ceil(math.log(1 / delta))
        self.m = math.ceil(math.e / epsilon)
        self.sketch = np.zeros((self.p, self.m))
    
    def add(self, key):
        '''
        Adds a hashable python object to the CMSketch.

        The function recieves one parameter, key, which corresponds
        to the object to add to the CMSketch.

        For each row of the matrix, a different random seed for the MMH3 hash function
        is used, which has shown good performance in experimental results for obtaining
        P pair-wise independent hash functions.
        '''


        for i in range(self.p):
            self.sketch[i, mmh3.hash(str(key), seed = i) % self.m] += 1
            
    def count(self, key):
        h = hash(key)
        return min([self.sketch[i, mmh3.hash(str(key), seed = i) % self.m] for i in range(self.p)])





class DyadicTree:
    '''
    A class for building a Dyadic Tree based on an interval [1,n]. This will consist
    on a binary tree made out of all the dyadic intervals contained in [1,n].
    A CMS will be associated whit each one of the heights of the tree.

    This class receives three parameters:

        - max_value: the maximum value that can appear in the stream.
        - epsilon & delta: parameters to build the CMS's for each height of the tree

    The method `add` updates all the CMS's when a new value from the stream arrives.

    The method `range_query` estimates the sum of the frequencies of all elements
    in a given interval [l,r]
    '''
    def __init__(self, max_value, epsilon, delta):
        self.height = math.ceil(math.log2(max_value))+1
        
        self.cm_sketch = [CountMinSketch(epsilon,delta) for h in range(self.height)]
                
    def add(self, value):
        x = 1
        for h in range(len(self.cm_sketch)):
            y = (self.height-1)-h
            self.cm_sketch[h].add(x)
            
            if h < len(self.cm_sketch)-1:
                left, right = dyadic_interval(x,y)
                mid = right-((right-left+1)//2)
                if value <= mid:
                    x = x*2-1
                else:
                    x = x*2
                    
    def range_query(self, l, r, x = 1, y = None):
        if y is None: y = self.height-1
        
        min_v, max_v = dyadic_interval(x,y)
        if l == min_v and r == max_v:
            return self.cm_sketch[(self.height-1)-y].count(x)
        
        mid = max_v-((max_v-min_v+1)//2)
        if r <= mid:
            return self.range_query(l, r, x = 2*x-1, y = y-1)
        elif l > mid:
            return self.range_query(l, r, x = 2*x, y = y-1)
        else:
            return self.range_query(l, mid, x = 2*x-1, y = y-1) + self.range_query(mid+1, r, x = 2*x, y = y-1)
            

