#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wkr.io` package."""

import gzip
import itertools
import os
import sys
import zipfile

import lzma
import pytest

import wkr
from wkr.compat import binary_type, text_type

BINARY_DATA = b'10011001'


@pytest.fixture
def binary_file(tmpdir):
    """Fixture to produce a binary file on disk."""
    filename = tmpdir.join('blob.bin').ensure().strpath
    with open(filename, 'wb') as output_file:
        output_file.write(BINARY_DATA)
    return filename


@pytest.fixture(params=[('bin', open),
                        ('xz', lzma.LZMAFile),
                        ('gz', gzip.open)])
def compressed_file(tmpdir, request):
    """Fixture to produce compressed files."""
    ext, open_fn = request.param
    path = tmpdir.join('test.{}'.format(ext)).ensure().strpath
    with open_fn(path, 'wb') as output_file:
        output_file.write(BINARY_DATA)
    return path


@pytest.fixture
def zip_file(tmpdir):
    """Fixture to produce a zip file."""
    filename = tmpdir.join('test.zip').ensure().strpath
    with zipfile.ZipFile(filename, 'w') as archive:
        for num in range(1, 4):
            contents = b'line {}'.format(num)
            contents += b'\n' + BINARY_DATA
            archive.writestr('file{}.txt'.format(num), contents)
    return filename


def test_open_finds_streams():
    """Test that wkr.open returns standard streams."""
    assert wkr.open('-', 'r') is sys.stdin
    assert wkr.open('-', 'rb') is sys.stdin
    assert wkr.open('-', 'w') is sys.stdout
    assert wkr.open('-', 'wb') is sys.stdout
    assert wkr.open('-', 'a') is sys.stdout
    assert wkr.open('-', 'ab') is sys.stdout


def test_read_compressed_file(compressed_file):
    """Test that wkr.open can read compressed file formats."""
    with wkr.open(compressed_file, 'rb') as input_file:
        data = input_file.read()
        assert isinstance(data, binary_type)
        assert data == BINARY_DATA


def test_already_open_file(binary_file):
    """Test that wkr.open passes through files that are already open."""
    with open(binary_file, 'rb') as input_file:
        for mode in ['r', 'a', 'w', 'rb', 'ab', 'wb']:
            assert wkr.open(input_file, mode) is input_file


def test_read_zip_file(zip_file):
    """Test that wkr.open can read zip files."""
    for num in range(1, 4):
        with wkr.open('{zip_file}:file{num}.txt'.format(
                zip_file=zip_file, num=num)) as input_file:
            contents = input_file.read()
            assert isinstance(contents, binary_type)
            contents = contents.split(b'\n')
            assert len(contents) == 2
            assert contents[0] == 'line {}'.format(num)
            assert contents[1] == BINARY_DATA


def test_write_compressed_file(compressed_file):
    """Test that wkr.open can write to compressed file formats."""
    contents = b'new file\n' + BINARY_DATA
    with wkr.open(compressed_file, 'wb') as output_file:
        output_file.write(contents)
    ext = os.path.splitext(compressed_file)[1]
    open_fn = {'.bin': open, '.xz': lzma.LZMAFile, '.gz': gzip.open}.get(ext)
    input_file = open_fn(compressed_file, 'rb')
    data = input_file.read()
    assert isinstance(data, binary_type)
    assert data == contents
    input_file.close()


def test_cannot_write_zip_file(zip_file):
    """Test that wkr.open cannot write to zip files."""
    modes = ['w', 'a', 'wb', 'ab']
    for mode in modes:
        with pytest.raises(Exception):
            _ = wkr.open('{}:file1.txt'.format(zip_file), mode)  # noqa f841


def test_cannot_open_non_files():
    """Test that wkr.open fails if it is passed something bad."""
    modes = ['r', 'rb', 'a', 'ab', 'w', 'wb']
    args = [
        (1,),               # tuple
        1,                  # int
        1.0,                # float
        {'key': 'value'},   # dict
        set(range(10)),     # set
        [1, 2, 3, 4],       # list
    ]
    for (arg, mode) in itertools.product(args, modes):
        with pytest.raises(Exception):
            _ = wkr.open(arg, mode)  # noqa f841
