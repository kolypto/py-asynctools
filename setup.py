#!/usr/bin/env python
""" Async tools for Python """

from setuptools import setup, find_packages

setup(
    # http://pythonhosted.org/setuptools/setuptools.html
    name='asynctools',
    version='0.1.2-2',
    author='Mark Vartanyan',
    author_email='kolypto@gmail.com',

    url='https://github.com/kolypto/py-asynctools',
    license='BSD',
    description=__doc__,
    long_description=open('README.rst').read(),
    keywords=['async', 'threading', 'multiprocessing'],

    packages=find_packages(),
    scripts=[],
    entry_points={},

    install_requires=[],
    extras_require={
        '_dev': ['wheel', 'nose'],
    },
    include_package_data=True,
    test_suite='nose.collector',

    platforms='any',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
    ],
)
