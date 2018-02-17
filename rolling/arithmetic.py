from collections import Counter, deque
from itertools import islice

from .base import RollingObject


class RollingSum(RollingObject):
    """Iterator object that computes the sum
    of a rolling window over a Python iterable.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(k)

    where k is the size of the rolling window

    Examples
    --------

    >>> seq = (8, 1, 1, 3, 6, 5)
    >>> r_sum = RollingSum(seq, 3)
    >>> next(r_sum)
    10
    >>> next(r_sum)
    5
    >>> r_sum = RollingSum(seq, 4)
    >>> list(r_sum)
    [13, 11, 15]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Sum':

    >>> from rolling import rolling
    >>> r_sum = rolling(seq, window_size=3, func='Sum')

    """
    _func_name = 'Sum'

    def _init_fixed(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._buffer.appendleft(0)
        self._sum = sum(self._buffer)

    def _init_variable(self, iterable, window_size, **kwargs):
        super().__init__(iterable, window_size, **kwargs)
        self._buffer = deque(maxlen=window_size)
        self._sum = 0

    def _update(self):
        value = next(self._iterator)
        self._sum += value - self._buffer.popleft()
        self._buffer.append(value)

    def _add_new(self):
        value = next(self._iterator)
        self._sum += value
        self._buffer.append(value)

    def _remove_old(self):
        self._sum -= self._buffer.popleft()

    @property
    def current_value(self):
        return self._sum

    @property
    def _obs(self):
        return len(self._buffer)
