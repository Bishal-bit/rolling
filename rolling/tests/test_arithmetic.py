import pytest

from rolling.apply import Apply
from rolling.arithmetic import Sum, Nunique

def _nunique(seq):
    "For testing Nunique - return count of unique items"
    return len(set(seq))

@pytest.mark.parametrize('array', [
    [3, 0, 1, 7, 2],
    [3, -8, 1, 7, -2, 4, 7, 2, 1],
    [1],
    [],
])
@pytest.mark.parametrize('window_size', list(range(1, 6)))
@pytest.mark.parametrize('window_type', ['fixed', 'variable'])
def test_rolling_sum(array, window_size, window_type):
    expected = Sum(array, window_size, window_type=window_type)
    got = Apply(array, window_size, operation=sum, window_type=window_type)
    assert list(got) == list(expected)


@pytest.mark.parametrize('word', [
    'aabbc',
    'xooxyzzziiismsdd',
    'jjjjjj',
    '',
])
@pytest.mark.parametrize('window_size', list(range(1, 6)))
@pytest.mark.parametrize('window_type', ['fixed', 'variable'])
def test_rolling_nunique(word, window_size, window_type):
    expected = Nunique(word, window_size, window_type=window_type)
    got = Apply(word, window_size, operation=_nunique, window_type=window_type)
    assert list(got) == list(expected)
