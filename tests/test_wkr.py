#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wkr.__init__` package."""

import itertools
import random
import string
import timeit

import pytest

import wkr


def random_value(val_type):
    """
    Create a random value of a given type.

    :param str val_type:
    """
    if val_type == 'd':
        return random.randint(0, 100000)
    elif val_type == 'l':
        return [random.randint(0, 100000)]
    elif val_type == 's':
        return random.choice(string.printable)
    elif val_type == 'S':
        return '{}'.format(random.randint(0, 100000))
    elif val_type == 't':
        return (random.randint(0, 100000), random.randint(0, 100000))


@pytest.fixture(params=list(itertools.product(['d', 'l', 's', 'S', 't'],
                                              [0, 1, 10, 100],
                                              [0, 1, 10, 100])))
def nested_lists(request):
    """Build a random list of random lists."""
    val_type, length, sub_length = request.param
    return [[random_value(val_type) for _ in range(sub_length)]
            for _ in range(length)]


@pytest.fixture(params=list(itertools.product(['d', 's', 'S', 't'],
                                              [0, 1, 10, 100],
                                              [0, 1, 10, 100])))
def list_of_sets(request):
    """Build a random list of random sets."""
    val_type, length, sub_length = request.param
    return [set(random_value(val_type) for _ in range(sub_length))
            for _ in range(length)]


def test_reduce_lists(nested_lists):
    """Test that wkr.reduce_lists flattens a variety of list values."""
    assert wkr.reduce_lists(nested_lists) == reduce(lambda a, b: a + b,
                                                    nested_lists, [])


def test_reduce_sets_or(list_of_sets):
    """Test that wkr.reduce_sets_or properly computes a union."""
    assert wkr.reduce_sets_or(list_of_sets) == reduce(lambda a, b: a | b,
                                                      list_of_sets, set())


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
    print __name__
    time = timeit.timeit(setup='from tests.test_wkr import fib, wkr; ',
                         stmt='fib(13)', number=10000)
    mtime = timeit.timeit(setup=('from tests.test_wkr import fib, wkr; '
                                 'mfib = wkr.memoize(fib)'),
                          stmt='mfib(13)', number=10000)
    assert mtime < time
