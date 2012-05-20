# -*- coding: utf-8 -*-
u"""

.. moduleauthor:: Mark Hall <mark.hall@mail.room3b.eu>
"""
from nose.tools import eq_

from pywebtools.text import (title)

def test_title():
    eq_('Test',
        title('Test'))
    eq_('Test',
        title('test'))
    eq_('TEST',
        title('TEST'))
    eq_('TEST',
        title('tEST'))
    eq_('',
        title(''))
    eq_('123',
        title('123'))
    