#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wkr.pd` package."""

import pandas as pd

from wkr.pd import pandas_memoize


def dataframe_gen():
    """Generate a number of DataFrames."""
    d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
         'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
    yield pd.DataFrame(d, index=['d', 'b', 'a'])
    df = pd.DataFrame(d, index=['d', 'b', 'a'],
                      columns=['two', 'three'])
    df['three'] = pd.to_numeric(df['three'])
    yield df
    yield pd.DataFrame({'one': [1., 2., 3., 4.],
                        'two': [4., 3., 2., 1.]},
                       index=['a', 'b', 'c', 'd'])
    yield pd.DataFrame([{'a': 1, 'b': 2},
                        {'a': 5, 'b': 10, 'c': 20}])


def test_memoize_pandas(tmpdir):
    """Test `wkr.pd.memoize_pandas`."""
    for idx, df in enumerate(dataframe_gen()):
        filename = tmpdir.join('data{}.csv'.format(idx))

        @pandas_memoize(filename.strpath)
        def f():
            return df

        assert not filename.exists()
        df2 = f()
        assert df2.equals(df)
        assert filename.exists()
        df3 = pd.read_csv(filename.strpath,
                          encoding='utf-8', index_col=0)
        assert df3.equals(df)
