# Range Queries using Count-Min Sketch

----------

## Overview

RangeQ_CMS is a Python implementation of the algorithm described in (Cormode and Muthukrishan 2005), that provides a method for the obtention of estimated Range Queries using Count-Min Sketch and Dyadic Intervals.

This method becomes useful with huge datasets where it is difficult (or even impossible) to store them in local memory, making the obtantion of basic statistics practically prohibitive.