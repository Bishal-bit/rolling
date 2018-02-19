# rolling

A collection of efficient rolling (i.e. sliding, moving) window algorithms for Python, with a easy-to-use iterface.

Arithmetical, logical and statistical functions are implemented. Both fixed-length and variable-length windows are supported.

## Overview

This module provides implementations of useful rolling-window operations, including sum, mean, and max. These operations can be applied over any iterable Python object, finite or infinite (lists, generators, files, and so on).

Naively applying builtin functions to a window (such as `sum()` and `max()`) becomes increasingly slow as window size increases (the complexity is typically **O(k)** where **k** is the size of the window).

However for many operations, there are algorithms that compute the value for each window in _constant_ time as window size increases, **O(1)**. The rolling window algorithms implemented so far in this module are summarised below:

| Operation                | Update   | Memory | Comments |
| ------------------------ |:--------:|:------:|-----------------------------|
| Sum                      | O(1)     | O(k)   | Sum of window values |
| Mean                     | O(1)     | O(k)   | Arithmetic mean of window |
| Median                   | O(log k) | O(k)   | Uses an indexable skiplist approach (proposed by R. Hettinger) |
| Var                      | O(1)     | O(k)   | Rolling variance, uses Welford's algorithm |
| Std                      | O(1)     | O(k)   | Rolling standard deviation, uses Welford's algorithm |
| Any                      | O(1)     | O(1)   | True if any value in the window is True, else False |
| All                      | O(1)     | O(1)   | True if all values in the window are True, else False |
| Count                    | O(1)     | O(k)   | Counts the number of True values in the window |
| Min                      | O(1)     | O(k)   | Uses the 'Ascending Minima' algorithm |
| Min2                     | O(1)     | O(k)*  | Uses heap to track minimum. Memory scales linearly with k over unordered data |
| Max                      | O(1)     | O(k)   | Uses the 'Descending Maxima' algorithm |

See the References section below for more details about the algorithms and links to other resources.

## Installation

There are no external library dependencies for running this module.

```
git clone https://github.com/ajcr/rolling.git
cd rolling/
pip install .
```
If you want to run the tests you'll need to install pytest; once done, just run `pytest` from the base directory.

## Quickstart

Import the `rolling()` function:
```python
>>> from rolling import rolling
```
Now suppose we have this list:
```python
>>> counts = [1, 5, 2, 0, 3]
```
The `rolling()` function creates an [iterator object](https://docs.python.org/3/library/stdtypes.html#iterator-types) over the list (or any other iterable) with a specified window size and reduction operation:
```python
>>> r_sum = rolling(counts, window_size=3, func='Sum') # rolling sum
>>> r_all = rolling(counts, window_size=3, func='All') # rolling all
>>> r_max = rolling(counts, window_size=3, func='Max') # rolling max
```
The result of iterating over each rolling object using `list()` is shown below. Note that the window type is fixed by default, meaning that only windows of the specified size (3) are used:
```python
>>> list(r_sum)
[8, 7, 5]

>>> list(r_all)
[True, False, False]

>>> list(r_max)
[5, 5, 3]
```
As well as the built-in efficient algorithms, any callable Python object can be applied to the rolling window when using the `rolling()` function:
```python
>>> r_list = rolling(counts, window_size=3, func=tuple)
>>> list(r_list)
[(1, 5, 2), (5, 2, 0), (2, 0, 3)]
```

Variable-length windows can be specified using the `window_type` argument. This allows windows smaller than the specified size to be evaluation at the beginning and end of the iterable. For instance:
```python
>>> r_list = rolling(counts, window_size=3, func=list, window_type='variable')
>>> list(r_list)
[[1],
 [1, 5],
 [1, 5, 2],
 [5, 2, 0],
 [2, 0, 3],
 [0, 3],
 [3]]
```

## Discussion and future work

The algorithms implemented by this module are chosen to be efficient in the sense that the cost of computing each new return value scales efficiently with the size of window.

In practice you might find that it is quicker *not* to use the the 'efficient' algorithm, and instead apply a function to the window. This is especially true for very small window sizes where the cost of updating a window is relatively complex. For instance, while the window size `k` is less than approximately 50, it may quicker to use `rolling(array, k, min)` (apply Python's builtin minimum function) rather than using `rolling(array, k, 'Min')`.

With this in mind, in future it might be worth implementing some of the algorithms here in compiled code (e.g. as a C extension module, or using Cython) to improve speed.

## References and resources

Some rolling algorithms are widely known (e.g. 'Sum' and 'Mean') and I am not sure which source to cite.

Other rolling algorithms are very cleverly designed and I learned a lot by reading about them and seeing other peoples' implementations. Here are the main resources that I used:

- **Max** and **Min** are implemented using the Ascending Minima and Descending Maxima algorithms described by Richard Harter [here](http://www.richardhartersworld.com/cri/2001/slidingmin.html). This algorithm is also used in [pandas](http://pandas.pydata.org/) and [bottleneck](https://github.com/kwgoodman/bottleneck). My attention was first drawn to this algorithm by Jaime Fernandez del Rio's excellent talk ['The Secret Life Of Rolling Pandas'](https://www.youtube.com/watch?v=XM_r5La-1tA). The algorithm is also described by Keegan Carruthers-Smith [here](https://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html), along with code examples.

- **Median** uses the indexable skiplist approach presented by Raymond Hettinger [here](http://code.activestate.com/recipes/577073/).

- **Var** and **Std** use [Welford's algorithm](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#On-line_algorithm). I referred to the rolling variance implementation in [pandas](https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/window.pyx#L635-L784) as well as an older edit of the Wikipedia page [Algorithms for calculating variance](https://en.wikipedia.org/w/index.php?title=Algorithms_for_calculating_variance&oldid=617145179).

