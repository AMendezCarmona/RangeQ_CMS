# Range Queries using Count-Min Sketch

## Overview

RangeQ_CMS is a Python implementation of the algorithm described in [(Cormode and Muthukrishan 2005)](https://github.com/AMendezCarmona/RangeQ_CMS#references), that provides a method for the obtention of estimated Range Queries using Count-Min Sketch and Dyadic Intervals.

This method becomes useful with huge datasets where it is difficult (or even impossible) to store them in local memory, making the obtantion of basic statistics practically prohibitive.


## Count-Min Sketch

Probabilistic data structure described in [(Cormode and Muthukrishan 2005)](https://github.com/AMendezCarmona/RangeQ_CMS#references) intended for storing a sublinear approximation of a given set. This method receives elements in a stream and can estimate the frequency of any element within a margin of error.

The data stucture consist of a two-dimensional $m \times p$. Given $\epsilon$ and $\delta$, CMS guarantees an estimation error within an additive error of $\epsilon$ with probability $\delta$. The dimension of the sketch can be then determined as $p = \lceil \ln(1/\delta) \rceil$ and $m = \lceil e/\epsilon \rceil$.

For a more detailed description of the data structure and its methods, see [(Cormode and Muthukrishan 2005)](https://github.com/AMendezCarmona/RangeQ_CMS#references).

## Range Queries using CMS

A range query computes the sum of the frequencies for all the elements between and interval $\[l,r\]$.


## References

<blockquote> Cormode, Graham, and Shan Muthukrishnan. "An improved data stream summary: the count-min sketch and its applications." Journal of Algorithms 55, no. 1 (2005): 58-75. </blockquote>