#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wkr.__init__` package."""

import itertools
import random
import string
import timeit
from functools import reduce

import pytest

import wkr


def random_value(val_type):
    """
    Create a random value of a given type.

    :param str val_type:
    """
    if val_type == "d":
        return random.randint(0, 100000)
    elif val_type == "l":
        return [random.randint(0, 100000)]
    elif val_type == "s":
        return random.choice(string.printable)
    elif val_type == "S":
        return "{}".format(random.randint(0, 100000))
    elif val_type == "t":
        return (random.randint(0, 100000), random.randint(0, 100000))


@pytest.fixture(
    params=list(
        itertools.product(["d", "l", "s", "S", "t"], [0, 1, 10, 100], [0, 1, 10, 100])
    )
)
def nested_lists(request):
    """Build a random list of random lists."""
    val_type, length, sub_length = request.param
    return [[random_value(val_type) for _ in range(sub_length)] for _ in range(length)]


@pytest.fixture(
    params=list(
        itertools.product(["d", "s", "S", "t"], [0, 1, 10, 100], [0, 1, 10, 100])
    )
)
def list_of_sets(request):
    """Build a random list of random sets."""
    val_type, length, sub_length = request.param
    return [
        set(random_value(val_type) for _ in range(sub_length)) for _ in range(length)
    ]


def test_reduce_lists(nested_lists):
    """Test that wkr.reduce_lists flattens a variety of list values."""
    assert wkr.reduce_lists(nested_lists) == reduce(
        lambda a, b: a + b, nested_lists, []
    )


def test_reduce_sets_or(list_of_sets):
    """Test that wkr.reduce_sets_or properly computes a union."""
    assert wkr.reduce_sets_or(list_of_sets) == reduce(
        lambda a, b: a | b, list_of_sets, set()
    )


def fib(num):
    """
    Get a value from the Fibonacci sequence.

    :param int num:
    """
    if num == 0:
        return 1
    if num == 1:
        return 1
    return fib(num - 2) + fib(num - 1)


def test_memoize_correct():
    """Test that memoize doesn't alter return values of a function."""
    mfib = wkr.memoize(fib)
    for num in range(12):
        assert fib(num) == mfib(num)


def test_memoize_fast():
    """Test that memoize speeds up a slow function."""
    time = timeit.timeit(
        setup="from tests.test_wkr import fib, wkr; ", stmt="fib(13)", number=10000
    )
    mtime = timeit.timeit(
        setup=("from tests.test_wkr import fib, wkr; " "mfib = wkr.memoize(fib)"),
        stmt="mfib(13)",
        number=10000,
    )
    assert mtime < time


def test_rle():
    """Test the wkr.rle method."""
    assert list(wkr.rle([])) == []
    assert list(wkr.rle([()])) == [((), 0, 1)]
    assert list(wkr.rle("aaaaa")) == [("a", 0, 5)]
    assert list(wkr.rle([1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1])) == [
        (1, 0, 4),
        (0, 4, 7),
        (1, 7, 13),
        (0, 13, 15),
        (1, 15, 16),
    ]
    assert list(wkr.rle([0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1])) == [
        (0, 0, 1),
        (1, 1, 5),
        (0, 5, 8),
        (1, 8, 14),
        (0, 14, 16),
        (1, 16, 17),
    ]
    assert list(wkr.rle([1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1])) == [
        (1, 0, 1),
        (0, 1, 2),
        (1, 2, 6),
        (0, 6, 9),
        (1, 9, 15),
        (0, 15, 17),
        (1, 17, 18),
    ]
    assert list(wkr.rle([1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0])) == [
        (1, 0, 1),
        (0, 1, 2),
        (1, 2, 6),
        (0, 6, 9),
        (1, 9, 15),
        (0, 15, 17),
    ]
    assert list(
        wkr.rle(
            [
                True,
                False,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
            ]
        )
    ) == [
        (True, 0, 1),
        (False, 1, 2),
        (True, 2, 6),
        (False, 6, 9),
        (True, 9, 15),
        (False, 15, 17),
    ]
    assert list(wkr.rle("aaAAaa")) == [("a", 0, 2), ("A", 2, 4), ("a", 4, 6)]
    assert list(wkr.rle("aaAAaa", keyfunc=lambda x: x.lower())) == [("a", 0, 6)]


def test_first():
    assert wkr.first(lambda x: x > 10, range(20)) == 11
    with pytest.raises(StopIteration):
        wkr.first(lambda x: x > 30, range(20))
    assert wkr.first(lambda x: x > 30, range(20), None) is None


def test_groupby():
    assert dict(wkr.groupby(range(10), lambda x: x < 5)) == {
        True: [0, 1, 2, 3, 4],
        False: [5, 6, 7, 8, 9],
    }
    assert dict(wkr.groupby([], lambda x: x < 5)) == {}
    test_list = [
        {"type": "A", "value": 123},
        {"type": "A", "value": 12},
        {"type": "B", "value": 123},
    ]
    assert dict(wkr.groupby(test_list, "type")) == {
        "A": [{"type": "A", "value": 123}, {"type": "A", "value": 12}],
        "B": [{"type": "B", "value": 123}],
    }
    assert dict(wkr.groupby(test_list, "value")) == {
        123: [{"type": "A", "value": 123}, {"type": "B", "value": 123}],
        12: [{"type": "A", "value": 12}],
    }
