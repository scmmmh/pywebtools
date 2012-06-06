# -*- coding: utf-8 -*-
u"""

.. moduleauthor:: Mark Hall <mark.hall@mail.room3b.eu>
"""
from genshi.builder import tag, Markup

from pywebtools.form import *

from pywebtools_test import geq

class TestError():
    
    def __init__(self, error_dict=None):
        if error_dict:
            self.error_dict = error_dict
        else:
            self.error_dict = None

def test_error_wrapper():
    content = tag.input(type='text', name='test', value='test')
    geq(content,
        error_wrapper(content, 'test', None))
    geq(content,
        error_wrapper(content, None, None))
    geq(content,
        error_wrapper(content, 'test', 'not an error'))
    geq(content,
        error_wrapper(content, 'test', TestError()))
    geq(content,
        error_wrapper(content, 'test', TestError({'another_field': 'Some error'})))
    geq(content,
        error_wrapper(content, None, TestError({'another_field': 'Some error'})))
    geq(content,
        error_wrapper(content, ['test1', 'test2'], TestError({'another_field': 'Some error'})))
    geq(tag.div(content, tag.p('The error message', class_='error-explanation'), class_='error'),
        error_wrapper(content, 'test', TestError({'test': 'The error message'})))
    geq(tag.div(content, tag.p('The error message', class_='error-explanation'), class_='error'),
        error_wrapper(content, ['test', 'test1'], TestError({'test': 'The error message'})))

def test_hidden_field():
    geq(tag.span(tag.input(type='hidden', name='name', value='value'), style='display:none;'),
        hidden_field('name', 'value'))

def test_csrf_token():
    geq(tag.span(tag.input(type='hidden', name='csrf_token', value='THE_TOKEN_VALUE'), style='display:none;'),
        csrf_token_field('THE_TOKEN_VALUE'))

def test_text_field():
    geq(tag.input(type='text', name='text_field', value='Initial value'),
        text_field('text_field', 'Initial value', None))

def test_number_field():
    geq(tag.input(type='number', name='number_field', value='Initial value'),
        number_field('number_field', 'Initial value', None))

def test_email_field():
    geq(tag.input(type='email', name='email_field', value='Initial value'),
        email_field('email_field', 'Initial value', None))

def test_url_field():
    geq(tag.input(type='url', name='url_field', value='Initial value'),
        url_field('url_field', 'Initial value', None))

def test_date_field():
    geq(tag.input(type='date', name='date_field', value='Initial value'),
        date_field('date_field', 'Initial value', None))

def test_time_field():
    geq(tag.input(type='time', name='time_field', value='Initial value'),
        time_field('time_field', 'Initial value', None))

def test_datetime_field():
    geq(tag.input(type='datetime', name='datetime_field', value='Initial value'),
        datetime_field('datetime_field', 'Initial value', None))

def test_month_field():
    geq(tag.input(type='month', name='month_field', value='Initial value'),
        month_field('month_field', 'Initial value', None))

def test_password_field():
    geq(tag.input(type='password', name='password_field'),
        password_field('password_field', None))

def test_file_field():
    geq(tag.input(type='file', name='file_field'),
        file_input_field('file_field', None))

def test_checkbox():
    geq(tag.input(type='checkbox', name='checkbox_field', value='selected'),
        checkbox('checkbox_field', 'selected', None))
    geq(tag(tag.input(type='checkbox', name='checkbox_field', value='selected', id='checkbox_field.selected'),
            Markup('&nbsp;'), tag.label('A label', for_='checkbox_field.selected')),
        checkbox('checkbox_field', 'selected', None, label='A label'))
    geq(tag(tag.input(type='checkbox', name='checkbox_field', value='selected', id='custom_id'),
            Markup('&nbsp;'), tag.label('A label', for_='custom_id')),
        checkbox('checkbox_field', 'selected', None, label='A label', id='custom_id'))
    geq(tag.input(type='checkbox', name='checkbox_field', value='selected', checked='checked'),
        checkbox('checkbox_field', 'selected', None, checked=True))
    geq(tag.input(type='checkbox', name='checkbox_field', value='selected', checked='checked'),
        checkbox('checkbox_field', 'selected', None, checked='checked'))
    geq(tag.input(type='checkbox', name='checkbox_field', value='selected', checked='checked'),
        checkbox('checkbox_field', 'selected', None, **{'checked': 'checked'}))
    geq(tag.input(type='checkbox', name='checkbox_field', value='selected', checked='checked'),
        checkbox('checkbox_field', 'selected', None, checked='whatever'))

def test_radio():
    geq(tag.input(type='radio', name='radio_field', value='selected'),
        radio('radio_field', 'selected', None))
    geq(tag(tag.input(type='radio', name='radio_field', value='selected', id='radio_field.selected'),
            Markup('&nbsp;'), tag.label('A label', for_='radio_field.selected')),
        radio('radio_field', 'selected', None, label='A label'))
    geq(tag(tag.input(type='radio', name='radio_field', value='selected', id='custom_id'),
            Markup('&nbsp;'), tag.label('A label', for_='custom_id')),
        radio('radio_field', 'selected', None, label='A label', id='custom_id'))
    geq(tag.input(type='radio', name='radio_field', value='selected', checked='checked'),
        radio('radio_field', 'selected', None, checked=True))
    geq(tag.input(type='radio', name='radio_field', value='selected', checked='checked'),
        radio('radio_field', 'selected', None, checked='checked'))
    geq(tag.input(type='radio', name='radio_field', value='selected', checked='checked'),
        radio('radio_field', 'selected', None, **{'checked': 'checked'}))
    geq(tag.input(type='radio', name='radio_field', value='selected', checked='checked'),
        radio('radio_field', 'selected', None, checked='whatever'))

def test_textarea():
    geq(tag.textarea('This is a text to edit', name='textarea'),
        textarea('textarea', 'This is a text to edit', None))

def test_select():
    geq(tag.select(tag.option('Value 1', value='value1'), tag.option('Value 2', value='value2'), name='select'),
        select('select', None, [('value1', 'Value 1'), ('value2', 'Value 2')], None))
    geq(tag.select(tag.option('Value 1', value='value1', selected='selected'), tag.option('Value 2', value='value2'), name='select'),
        select('select', 'value1', [('value1', 'Value 1'), ('value2', 'Value 2')], None))
    geq(tag.select(tag.option('Value 1', value='value1', selected='selected'), tag.option('Value 2', value='value1', selected='selected'), name='select'),
        select('select', 'value1', [('value1', 'Value 1'), ('value1', 'Value 2')], None))
    
def test_button():
    geq(tag.input(type='button', value='Press this button'),
        button('Press this button'))

def test_reset():
    geq(tag.input(type='reset', value='Reset this form'),
        reset('Reset this form'))

def test_submit():
    geq(tag.input(type='submit', value='Submit this form'),
        submit('Submit this form'))

