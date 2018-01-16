from collections import deque
from itertools import islice

from .base import RollingObject


class RollingAll(RollingObject):
    """Iterator object that computes whether all
    values in a rolling window over a Python iterable
    evaluate to True.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(1)

    Examples
    --------

    >>> seq = (8, 0, 1, 3, 6, 5)
    >>> r_all = RollingAll(seq, 3)
    >>> next(r_all)
    False
    >>> next(r_all)
    False
    >>> r_all = RollingSum(seq, 4)
    >>> list(r_all)
    [False, False, True]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'All':

    >>> from rolling import rolling
    >>> r_all = rolling(seq, window_size=3, func='All')

    """
    _func_name = 'All'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._consecutive_true = 0
        for _ in range(window_size - 1):
            self._update()

    def _update(self):
        if next(self._iterator):
            self._consecutive_true += 1
        else:
            self._consecutive_true = 0

    def __next__(self):
        self._update()
        return self._consecutive_true >= self.window_size


class RollingAny(RollingObject):
    """Iterator object that computes whether any
    values in a rolling window over a Python iterable
    evaluate to True.

    Parameters
    ----------

    iterable : any iterable object
    window_size : integer, the size of the rolling
        window moving over the iterable

    Complexity
    ----------

    Update time:  O(1)
    Memory usage: O(1)

    Examples
    --------

    >>> seq = (1, 0, 0, 0, 6, 5)
    >>> r_any = RollingAny(seq, 3)
    >>> next(r_any)
    True
    >>> next(r_any)
    False
    >>> r_any = RollingAny(seq, 4)
    >>> list(r_any)
    [True, True, True]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Any':

    >>> from rolling import rolling
    >>> r_any = rolling(seq, window_size=3, func='Any')

    """
    _func_name = 'Any'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)
        self._last_true = 0
        for _ in range(window_size - 1):
            self._update()

    def _update(self):
        if next(self._iterator):
            self._last_true = self.window_size
        else:
            self._last_true -= 1

    def __next__(self):
        self._update()
        return self._last_true > 0


class RollingCount(RollingObject):
    """Iterator object that counts the number of
    values in a rolling window over a Python iterable
    which evaluate to True.

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

    >>> seq = (1, 0, 0, 0, 6, 5)
    >>> r_count = RollingCount(seq, 3)
    >>> next(r_count)
    1
    >>> next(r_count)
    0
    >>> r_count = RollingCount(seq, 4)
    >>> list(r_count)
    [1, 1, 2]

    Notes
    -----

    This object can also be instantiated using the
    `rolling()` function by passing 'Count':

    >>> from rolling import rolling
    >>> r_count = rolling(seq, window_size=3, func='Count')

    """
    _func_name = 'Count'

    def __init__(self, iterable, window_size):
        super().__init__(iterable, window_size)

        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(map(bool, head), maxlen=window_size)
        self._buffer.appendleft(False)
        self._count = sum(self._buffer)

    def _update(self):
        value = bool(next(self._iterator))
        self._count += value - self._buffer.popleft()
        self._buffer.append(value)

    def __next__(self):
        self._update()
        return self._count
