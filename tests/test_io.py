#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wkr.io` package."""

import gzip
import lzma
import pytest

import wkr
from wkr.compat import binary_type, text_type

BINARY_DATA = b'10011001'

@pytest.fixture(params=[('bin', open), ('xz', lzma.LZMAFile), ('gz', gzip.open)])
def binary_file(tmpdir, request):
    ext, open_fn = request.param
    path = tmpdir.join("test.{}".format(ext))
    path.ensure()
    with open_fn(path.strpath, 'wb') as output_file:
        output_file.write(BINARY_DATA)
    return path.strpath

def test_read_xz(binary_file):
    with wkr.open(binary_file, mode='rb') as input_file:
        data = input_file.read()
        assert isinstance(data, binary_type)
        assert data == BINARY_DATA
    with wkr.open(binary_file, mode='r') as input_file:
        data = input_file.read()
        assert isinstance(data, text_type)
        assert data == BINARY_DATA.decode('utf-8')
