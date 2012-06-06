# -*- coding: utf-8 -*-
# Copyright 2012 Mark Hall (Mark.Hall@work.room3b.eu)
# 
# This file is part of the PyWebTools.
# 
# The PyWebTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The PyWebTools are distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with PyWebTools. If not, see <http://www.gnu.org/licenses/>.
'''
:mod:`pywebtools.form`
======================

This module provides a number of helper functions for generating form elements
using the `<http://genshi.edgewall.org/>`_ framework.

Each helper function will take an optional error object and if the name of the
form field is mapped to an error in the error object, then wrapper elements will
be added around the field to highlight the error and show the error message. It
is designed to work with the error objects provided by `<http://www.formencode.org>`_
(:py:class:`formencode.api.Invalid`), but will happily work with any error object that has a ``error_dict`` attribute,
which maps form field names to error messages.
'''

from genshi.builder import tag, Markup

def error_wrapper(content, field, e):
    if field and e and hasattr(e, 'error_dict') and e.error_dict:
        if isinstance(field, list):
            for field in field:
                if field in e.error_dict:
                    return tag.div(content,
                                   tag.p(e.error_dict[field], class_='error-explanation'),
                                   class_="error")
            return content
        elif field in e.error_dict:
            return tag.div(content,
                           tag.p(e.error_dict[field], class_='error-explanation'),
                           class_="error")
        else:
            return content
    else:
        return content

def hidden_field(name, value, **attr):
    '''Generates a hidden input field with the given name and value.
    
    Wraps the hidden field in a span element that is set to "display:none".
    
    :param name: The name of the hidden field to generate
    :param value: The value to set in the hidden field
    '''
    return tag.span(tag.input(type="hidden", name=name, value=value, **attr), style='display:none;')

def csrf_token_field(token):
    '''Generates a hidden input field with the name "csrf_token" and the given token
    value.
    
    :param token: The CSRF token value to set in the hidden field
    '''
    return hidden_field('csrf_token', token)

def text_field(name, text, e, **attr):
    '''Generates a text field with the given name and default text. All further
    parameters are passed on to Genshi.
    
    :param name: The field name
    :param text: The default value
    :param e: The error object
    '''
    return error_wrapper(tag.input(type='text', name=name, value=text, **attr), name, e)

def number_field(name, text, e, **attr):
    return error_wrapper(tag.input(type='number', name=name, value=text, **attr), name, e)

def email_field(name, text, e, **attr):
    return error_wrapper(tag.input(type='email', name=name, value=text, **attr), name, e)

def url_field(name, text, e, **attr):
    return error_wrapper(tag.input(type='url', name=name, value=text, **attr), name, e)

def date_field(name, text, e, **attr):
    return error_wrapper(tag.input(type='date', name=name, value=text, **attr), name, e)

def time_field(name, text, e, **attr):
    return error_wrapper(tag.input(type='time', name=name, value=text, **attr), name, e)

def datetime_field(name, text, e, **attr):
    return error_wrapper(tag.input(type='datetime', name=name, value=text, **attr), name, e)

def month_field(name, text, e, **attr):
    return error_wrapper(tag.input(type='month', name=name, value=text, **attr), name, e)

def password_field(name, e, **attr):
    return error_wrapper(tag.input(type='password', name=name, **attr), name, e)

def file_input_field(name, e, **attr):
    return error_wrapper(tag.input(type='file', name=name, **attr), name, e)

def checkbox(name, value, e, checked=False, label=None, **attr):
    if checked:
        attr['checked'] = 'checked'
    if label:
        if 'id' not in attr:
            attr['id'] = '%s.%s' % (name, value)
        return error_wrapper(tag(tag.input(type='checkbox', name=name, value=value, **attr),
                                 Markup('&nbsp;'),
                                 tag.label(label, for_=attr['id'])),
                             name, e)
    else:
        return error_wrapper(tag.input(type='checkbox', name=name, value=value, **attr), name, e)

def radio(name, value, e, checked=False, label=None, **attr):
    if checked:
        attr['checked'] = 'checked'
    if label:
        if 'id' not in attr:
            attr['id'] = '%s.%s' % (name, value)
        return error_wrapper(tag(tag.input(type='radio', name=name, value=value, **attr),
                                 Markup('&nbsp;'),
                                 tag.label(label, for_=attr['id'])),
                             name, e)
    else:
        return error_wrapper(tag.input(type='radio', name=name, value=value, **attr), name, e)

def textarea(name, text, e, **attr):
    return error_wrapper(tag.textarea(text, name=name, **attr), name, e)

def select(name, value, options, e, **attr):
    select_options = []
    for option in options:
        if option[0] == value:
            select_options.append(tag.option(option[1], value=option[0], selected="selected"))
        else:
            select_options.append(tag.option(option[1], value=option[0]))
    return error_wrapper(tag.select(select_options, name=name, **attr), name, e)

def button(label, **attr):
    return tag.input(type='button', value=label, **attr)

def reset(label, **attr):
    return tag.input(type='reset', value=label, **attr)

def submit(label, **attr):
    return tag.input(type='submit', value=label, **attr)
