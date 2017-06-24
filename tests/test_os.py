#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wkr.os` package."""

from wkr.os import mkdir_p


def test_mkdir_p_single(tmpdir):
    """Test mkdir_p on creating a single directory."""
    path = tmpdir.join('newdir')
    assert not path.exists()
    mkdir_p(path.strpath)
    assert path.exists()


def test_mkdir_p_double(tmpdir):
    """Test mkdir_p on creating two directories."""
    path1 = tmpdir.join('newdir2')
    assert not path1.exists()
    path2 = path1.join('subdir')
    assert not path2.exists()
    mkdir_p(path2.strpath)
    assert path1.exists()
    assert path2.exists()


def test_mkdir_p_exists(tmpdir):
    """Test mkdir_p on creating a directory that already exists."""
    path = tmpdir.join('newdir').ensure(dir=True)
    assert path.exists()
    assert path.isdir()
    mkdir_p(path.strpath)  # should not throw an exception
