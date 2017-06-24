#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wkr.os` package."""

import pytest

from wkr.os import mkdir_p


def test_mkdir_p_single(tmpdir):
    path = tmpdir.join('newdir')
    assert not path.exists()
    mkdir_p(path.strpath)
    assert path.exists()


def test_mkdir_p_double(tmpdir):
    path = tmpdir.join('newdir2').join('subdir')
    assert not path.exists()
    mkdir_p(path.strpath)
    assert path.exists()


def test_mkdir_p_exists(tmpdir):
    path = tmpdir.join('newdir').ensure(dir=True)
    assert path.exists()
    assert path.isdir()
    mkdir_p(path.strpath)  # should not throw an exception
