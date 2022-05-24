
import math
import numpy as np
import random
import sys
from heapdict import heapdict
from collections import defaultdict
import mmh3
import matplotlib.pyplot as plt


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

        - epsilon: factor fo estimation error, [0,1]
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
    def __init__(self, max_value, epsilon, delta):
        # El método recibe como argumentos el mayor valor que puede aparecer
        # en el stream, y los parámetros epsilon y delta para generar
        # los Count-Min Sketches
        
        # La altura del árbol es calculada como el log2 del valor máximo
        # (redondeado al alza, por si el valor no fuera potencia de 2) más 1
        self.height = math.ceil(math.log2(max_value))+1
        
        # Se genera una lista con un Count-Min Sketch por cada altura
        self.cm_sketch = [CountMinSketch(epsilon,delta) for h in range(self.height)]
                
    def add(self, value):
        # Este algoritmo añade, para cada intervalo Dxy
        # en el que esta presente el último valor del stream,
        # el elemento x al Count-Min Sketch asociado a la altura
        # en la que se encuentra Dxy en el árbol diádico
        
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
        # Una explicación detallada del algoritmo para encontrar
        # el conjunto de mínima cobertura de un árbol diádico se encuentra
        # al final del notebook.
        
        # Sumamos, para cada intervalo diádico Dxy en el conjunto de mínima
        # cobertura, la estimación de frecuencia del elemento x del Count Min Sketch
        # asociado a la altura del árbol en el que se encuentra el intervalo
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
            

