import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.RST')).read()
CHANGES = open(os.path.join(here, 'CHANGES.RST')).read()

requires = [
    'kajiki',
    'sqlalchemy',
    'formencode',
    'pyramid',
    'decorator',
    'transaction',
    'zope.sqlalchemy',
    'webtest'
    ]

setup(name='PyWebTools',
      version='1.0.5',
      description='A collection of helpers for use with Pyramid, Kajiki, Formencode, and SQLAlchemy',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
                   'Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 3',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                   'Operating System :: OS Independent'
        ],
      author='Mark Hall',
      author_email='Mark.Hall@work.room3b.eu',
      url='http://bitbucket.org/mhall/pywebtools/overview',
      keywords='web pyramid kajiki formencode SQLAlchemy',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires = requires,
      entry_points="""
      [pytest11]
      pywebtools_testing = pywebtools.testing
      """
      )
