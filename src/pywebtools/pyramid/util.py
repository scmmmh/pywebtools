# -*- coding: utf-8 -*-
"""
###############################################################
:mod:`pywebtools.pyramid.util` -- Utility Functions for Pyramid
###############################################################

Utility functions for use with the Pyramid framework.

* :func:`~pywebtools.pyramid.util.request_from_args` is useful with decorators
  or any other function where you do not know which argument is the Pyramid
  :class:`~pyramid.request.Request`.
* :func:`~pywebtools.pyramid.util.get_config_setting` provides easy access
  to configuration settings set in the [app:main] section of the INI file.
* :func:`~pywebtools.pyramid.util.require_method` is a decorator to enforce
  HTTP methods.
* :class:`~pywebtools.pyramid.util.MenuBuilder` is a helper class to generate
  the menu structure used with :func:`~pywebtools.kajiki.menubar`.

.. moduleauthor:: Mark Hall <mark.hall@work.room3b.eu>
"""
import json
import math

from pyramid.request import Request


def request_from_args(*args):
    """Returns the :class:`~pyramid.request.Request` from the function
    parameters list ``args``.

    :param args: The parameters passed to a function
    :return: The request object
    :r_type: :class:`~pyramid.request.Request`
    """
    for arg in args:
        if isinstance(arg, Request):
            return arg
    raise Exception('No request found')


def convert_type(value, target_type, default=None):
    """Attempts to convert the ``value`` to the given ``target_type``. Will
    return ``default`` if the conversion fails.

    Supported ``target_type`` values are:

    * `int` -- Convert to an integer value
    * `boolean` -- Convert to a boolean value (``True`` if the value is the
      ``unicode`` string "true" in any capitalisation
    * `list` -- Convert to a list, splitting on line-breaks and commas

    :param value: The value to convert
    :type value: `unicode`
    :param target_type: The target type to convert to
    :type target_type: `unicode`
    :param default: The default value if the conversion fails
    :return: The converted value
    """
    if target_type == 'int':
        try:
            return int(value)
        except ValueError:
            return default
    elif target_type == 'boolean':
        if value and value.lower() == 'true':
            return True
        else:
            return False
    elif target_type == 'list':
        return [v.strip() for line in value.split('\n') for v in line.split(',') if v.strip()]
    if value:
        return value
    else:
        return default


# Cached application settings for faster access
CACHED_SETTINGS = {}


def get_config_setting(request, key, target_type=None, default=None):
    """Gets a configuration setting from the application configuration.
    Settings are cached for faster access.

    :param request: The request used to access the configuration settings
    :type request: :class:`~pyramid.request.Request`
    :param key: The configuration key
    :type key: `unicode`
    :param target_type: If specified, will convert the configuration setting
                        to the given type using :func:`~pywebtools.pyramid.util.convert_type`
    :type default: The default value to return if there is no setting with the
                   given key
    :return: The configuration setting value or ``default``
    """
    global CACHED_SETTINGS
    if key in CACHED_SETTINGS:
        return CACHED_SETTINGS[key]
    else:
        if key in request.registry.settings:
            if target_type:
                CACHED_SETTINGS[key] = convert_type(request.registry.settings[key], target_type, default=default)
            else:
                CACHED_SETTINGS[key] = request.registry.settings[key]
        else:
            CACHED_SETTINGS[key] = default
        return get_config_setting(request, key, target_type=target_type, default=default)


class MenuBuilder(object):
    """The :class:`~pywebtools.pyramid.util.MenuBuilder` helps with creating the ``list``
    structure used for creating the icon-menubar used with :func:`~pywebtools.kajiki.menubar`.
    Call :func:`~pywebtools.pyramid.util.MenuBuilder.group` to start a new group of menu items.
    Call :func:`~pywebtools.pyramid.util.MenuBuilder.item` to add a menu item to the current group.
    :func:`~pywebtools.pyramid.util.MenuBuilder.generate` then generates the final structure for use in the menubar.
    """

    def __init__(self):
        self._groups = []
        self._group = None

    def group(self, label, icon=None):
        """Add a new group to the list of groups in this :class:`~pywebtools.pyramid.util.MenuBuilder`.

        :param label: The menu group's label
        :type label: `unicode`
        :param icon: The optional icon for this group. An icon must be provided in order to
                     enable highlighting of menu items
        :type icon: `unicode`
        """
        if self._group and self._group['items']:
            self._groups.append(self._group)
        self._group = {'label': label,
                       'items': []}
        if icon:
            self._group['icon'] = icon

    def menu(self, label, href, icon=None, highlight=False, attrs=None):
        """Add a new menu item to the current group. Will create a new group with an empty
        label if :func:`~pywebtools.pyramid.util.MenuBuilder.group` has not been called.

        :param label: The menu item's label
        :type label: `unicode`
        :param href: The URL that the menu item loads
        :type href: `unicode`
        :param icon: The optional icon for this menu item
        :type icon: `unicode`
        :param highlight: Whether to highlight the menu item by displaying it at the top level
        :type highlight: `boolean`
        :param attrs: Additional attributes to set for the menu item link
        :type attrs: :class:`dict`
        """
        if not self._group:
            self._group = {'label': '',
                           'items': []}
        if attrs:
            attrs['href'] = href
        else:
            attrs = {'href': href}
        item = {'visible': True,
                'label': label,
                'attrs': attrs}
        if icon:
            item['icon'] = icon
        if highlight:
            item['highlight'] = True
        self._group['items'].append(item)

    def generate(self):
        """Generate the final menu structure.

        :return: The list of menu groups with their menu items
        :return_type: ``list`` of menu groups
        """
        if self._group and self._group['items']:
            self._groups.append(self._group)
            self._group = None
        return self._groups


def paginate(request, route_name, query, start, rows, query_params=None):
    """Generates the list of pages for a query.

    :param request: The request used to generate URLs
    :type request: :class:`~pyramid.request.Request`
    :param route_name: The name of the route to use for URLs
    :type route_name: :py:func:`str`
    :param query: The SQLAlchemy query to generate the pagination for
    :type query: :class:`~sqlalchemy.orm.query.Query`
    :param start: The current starting index
    :type start: :py:func:`int`
    :param rows: The number of rows per page
    :type rows: :py:func:`int`
    :param query_params: An optional list of query parameters to include in all
                         URLs that are generated
    :type query_params: :py:func:`list` of :py:func:`tuple`
    :return: The :py:func:`list` of pages to use with the "navigation.pagination"
             helper
    :rtype: :py:func:`list`
    """
    if query_params is None:
        query_params = []
    else:
        query_params = [param for param in query_params if param[0] != 'start']
    count = query.count()
    pages = []
    if start > 0:
        pages.append({'type': 'prev',
                      'url': request.route_url(route_name, _query=query_params + [('start', max(start - rows, 0))])})
    else:
        pages.append({'type': 'prev'})
    for idx in range(0, int(math.ceil(count / float(rows)))):
        if idx == (start / rows):
            pages.append({'type': 'current',
                          'label': str(idx + 1)})
        else:
            pages.append({'type': 'item',
                          'label': str(idx + 1),
                          'url': request.route_url(route_name, _query=query_params + [('start', idx * rows)])})
    if start + rows < count:
        pages.append({'type': 'next',
                      'url': request.route_url(route_name, _query=query_params + [('start', min(start + rows, count))])})
    else:
        pages.append({'type': 'next'})
    return pages


def confirm_action(title, message, cancel, ok):
    """Generates a confirmation JSON object for use with the jQuery.postLink() plugin.

    :param title: The title of the confirmation dialog box
    :type title: ``unicode``
    :param message: The main message to show
    :type message: ``unicode``
    :param cancel: The cancel button's settings
    :type cancel: ``dict`` or ``unicode``
    :param ok: The ok button's settings
    :type ok: ``dict`` or ``unicode``
    :return: JSON object
    :rtype: :func:`unicode`
    """
    return json.dumps({'title': title,
                       'msg': message,
                       'cancel': cancel if isinstance(cancel, dict) else {'label': cancel},
                       'ok': ok if isinstance(ok, dict) else {'label': ok}})


def confirm_delete(obj_type, title, has_parts=False):
    """Generates the confirmation JSON object for use with the jQuery.postLink() plugin.

    :param obj_type: The type of object that is being deleted
    :type obj_type: ``unicode``
    :param title: The title of the object that is being delete
    :type title: ``unicode``
    :param has_parts: Whether to add the suffix " and all its parts"
    :type has_parts: ``bool``
    :return: JSON object
    :rtype: :func:`unicode`
    """
    msg = 'Please confirm that you wish to delete the %s "%s"' % (obj_type, title)
    if has_parts:
        msg = '%s and all its parts.' % (msg)
    else:
        msg = '%s.' % (msg)
    return confirm_action('Delete this %s' % (obj_type),
                          msg,
                          "Don't delete",
                          {'label': 'Delete',
                           'class_': 'alert'})
