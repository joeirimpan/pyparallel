# -*- coding: utf-8 -*-
import sys
import os

import pytest

testpath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testpath + '/../')

from pyparallel import Downloader # noqa


@pytest.fixture
def downloder():
    return Downloader(
        url='https://upload.wikimedia.org/wikipedia/commons/f/ff/Pizigani_1367_Chart_10MB.jpg',  # noqa
        conns=10,
        filename='chart.jpg'
    )
