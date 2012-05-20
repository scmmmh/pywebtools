# -*- coding: utf-8 -*-
u"""

.. moduleauthor:: Mark Hall <mark.hall@mail.room3b.eu>
"""
from genshi.builder import tag, Markup

from pywebtools.ui import (breadcrumbs, menu, pager)

from pywebtools_test import geq

def test_breadcrumbs():
    geq(tag.nav(tag.ol(), class_='breadcrumbs'),
        breadcrumbs([]))
    geq(tag.nav(tag.ol(tag.li(tag.a('Example', href='http://www.example.com'), class_='current')), class_='breadcrumbs'),
        breadcrumbs([('Example', {'href': 'http://www.example.com'})]))
    geq(tag.nav(tag.ol(tag.li(tag.a('Example 1', href='http://www.example.com/1.html')),
                       tag.li(tag.a('Example 2', href='http://www.example.com/2.html'), class_='current')), class_='breadcrumbs'),
        breadcrumbs([('Example 1', {'href': 'http://www.example.com/1.html'}), ('Example 2', {'href': 'http://www.example.com/2.html'})]))

def test_menu():
    geq(tag.nav(tag.ul()),
        (menu([], '')))
    geq(tag.nav(tag.ul(), class_='main-menu'),
        menu([], '', class_='main-menu'))
    geq(tag.nav(tag.ul(tag.li(tag.a('Example 1', href='http://www.example.com/1.html')),
                       tag.li(tag.a('Example 2', href='http://www.example.com/2.html')))),
        menu([('example1', 'Example 1', {'href': 'http://www.example.com/1.html'}), ('example2', 'Example 2', {'href': 'http://www.example.com/2.html'})], ''))
    geq(tag.nav(tag.ul(tag.li(tag.a('Example 1', href='http://www.example.com/1.html'), class_='current'),
                       tag.li(tag.a('Example 2', href='http://www.example.com/2.html')))),
        menu([('example1', 'Example 1', {'href': 'http://www.example.com/1.html'}), ('example2', 'Example 2', {'href': 'http://www.example.com/2.html'})], 'example1'))

def test_pager():
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')), tag.li(Markup('&lt;&nbsp;previous')), tag.li(Markup('next&nbsp;&gt;')), tag.li(Markup('last&nbsp;&raquo;'))), class_='pager'),
        pager('', 0, 0))
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')), tag.li(Markup('&lt;&nbsp;previous')), tag.li(tag.a(1, href='http://www.example.com?page=1'), class_='current'), tag.li(Markup('next&nbsp;&gt;')), tag.li(Markup('last&nbsp;&raquo;'))), class_='pager'),
        pager('http://www.example.com', 1, 1))
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')), tag.li(Markup('&lt;&nbsp;previous')), tag.li(tag.a(1, href='http://www.example.com?page=1'), class_='current'), tag.li(Markup('next&nbsp;&gt;')), tag.li(Markup('last&nbsp;&raquo;'))), class_='small pager'),
        pager('http://www.example.com', 1, 1, class_='small'))
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')), tag.li(Markup('&lt;&nbsp;previous')), tag.li(tag.a(1, href='http://www.example.com?page=1'), class_='current'), tag.li(Markup('next&nbsp;&gt;')), tag.li(Markup('last&nbsp;&raquo;'))), class_='pager'),
        pager('http://www.example.com', 1, 1, class_='pager'))
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')), tag.li(Markup('&lt;&nbsp;previous')), tag.li(tag.a(1, href='http://www.example.com?page=1'), class_='current'), tag.li(Markup('next&nbsp;&gt;')), tag.li(Markup('last&nbsp;&raquo;'))), class_='pager'),
        pager('http://www.example.com?', 1, 1))
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')), tag.li(Markup('&lt;&nbsp;previous')), tag.li(tag.a(1, href='http://www.example.com?p=v&page=1'), class_='current'), tag.li(Markup('next&nbsp;&gt;')), tag.li(Markup('last&nbsp;&raquo;'))), class_='pager'),
        pager('http://www.example.com?p=v', 1, 1))
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')), tag.li(Markup('&lt;&nbsp;previous')), tag.li(tag.a(1, href='http://www.example.com?p=v&page=1'), class_='current'), tag.li(Markup('next&nbsp;&gt;')), tag.li(Markup('last&nbsp;&raquo;'))), class_='pager'),
        pager('http://www.example.com?p=v&', 1, 1))
    geq(tag.nav(tag.ol(tag.li(tag.a(Markup('&laquo;&nbsp;first'), href='http://www.example.com?page=1')),
                       tag.li(tag.a(Markup('&lt;&nbsp;previous'), href='http://www.example.com?page=1')),
                       tag.li(tag.a(1, href='http://www.example.com?page=1')),
                       tag.li(tag.a(2, href='http://www.example.com?page=2'), class_='current'),
                       tag.li(tag.a(3, href='http://www.example.com?page=3')),
                       tag.li(tag.a(Markup('next&nbsp;&gt;'), href='http://www.example.com?page=3')),
                       tag.li(tag.a(Markup('last&nbsp;&raquo;'), href='http://www.example.com?page=3'))), class_='pager'),
        pager('http://www.example.com', 2, 3))
    geq(tag.nav(tag.ol(tag.li(tag.a(Markup('&laquo;&nbsp;first'), href='http://www.example.com?page=1')),
                       tag.li(tag.a(Markup('&lt;&nbsp;previous'), href='http://www.example.com?page=4')),
                       tag.li(tag.a(3, href='http://www.example.com?page=3')),
                       tag.li(tag.a(4, href='http://www.example.com?page=4')),
                       tag.li(tag.a(5, href='http://www.example.com?page=5'), class_='current'),
                       tag.li(tag.a(6, href='http://www.example.com?page=6')),
                       tag.li(tag.a(7, href='http://www.example.com?page=7')),
                       tag.li(tag.a(Markup('next&nbsp;&gt;'), href='http://www.example.com?page=6')),
                       tag.li(tag.a(Markup('last&nbsp;&raquo;'), href='http://www.example.com?page=10'))), class_='pager'),
        pager('http://www.example.com', 5, 10))
    geq(tag.nav(tag.ol(tag.li(Markup('&laquo;&nbsp;first')),
                       tag.li(Markup('&lt;&nbsp;previous')),
                       tag.li(tag.a(1, href='http://www.example.com?page=1'), class_='current'),
                       tag.li(tag.a(2, href='http://www.example.com?page=2')),
                       tag.li(tag.a(3, href='http://www.example.com?page=3')),
                       tag.li(tag.a(4, href='http://www.example.com?page=4')),
                       tag.li(tag.a(5, href='http://www.example.com?page=5')),
                       tag.li(tag.a(Markup('next&nbsp;&gt;'), href='http://www.example.com?page=2')),
                       tag.li(tag.a(Markup('last&nbsp;&raquo;'), href='http://www.example.com?page=10'))), class_='pager'),
        pager('http://www.example.com', 1, 10))
    geq(tag.nav(tag.ol(tag.li(tag.a(Markup('&laquo;&nbsp;first'), href='http://www.example.com?page=1')),
                       tag.li(tag.a(Markup('&lt;&nbsp;previous'), href='http://www.example.com?page=9')),
                       tag.li(tag.a(6, href='http://www.example.com?page=6')),
                       tag.li(tag.a(7, href='http://www.example.com?page=7')),
                       tag.li(tag.a(8, href='http://www.example.com?page=8')),
                       tag.li(tag.a(9, href='http://www.example.com?page=9')),
                       tag.li(tag.a(10, href='http://www.example.com?page=10'), class_='current'),
                       tag.li(Markup('next&nbsp;&gt;')),
                       tag.li(Markup('last&nbsp;&raquo;'))), class_='pager'),
        pager('http://www.example.com', 10, 10))
