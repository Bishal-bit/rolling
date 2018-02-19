from collections import deque
from itertools import islice

from .base import RollingObject


class Apply(RollingObject):
    """Apply a specific function to a rolling window"""

    def _init_fixed(self, iterable, window_size, func=sum, **kwargs):
        head = islice(self._iterator, window_size - 1)
        self._buffer = deque(head, maxlen=window_size)
        self._func = func

    def _init_variable(self, iterable, window_size, func=sum, **kwargs):
        self._buffer = deque(maxlen=window_size)
        self._func = func

    @property
    def current_value(self):
        return self._func(self._buffer)

    def _add_new(self):
        self._buffer.append(next(self._iterator))

    def _remove_old(self):
        self._buffer.popleft()

    def _update(self):
        self._buffer.append(next(self._iterator))

    @property
    def _obs(self):
        return len(self._buffer)

    def __repr__(self):
        return "Rolling(func='{}', window_size={}, window_type='{}')".format(
                    self._func.__name__, self.window_size, self.window_type)
