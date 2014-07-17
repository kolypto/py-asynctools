#!/usr/bin/env python
""" Async tools for Python """

from setuptools import setup, find_packages

setup(
    # http://pythonhosted.org/setuptools/setuptools.html
    name='asynctools',
    version='0.0.1-0',
    author='Mark Vartanyan',
    author_email='mark@dignio.com',

    url='https://github.com/kolypto/py-asynctools',
    license='BSD',
    description=__doc__,
    long_description=open('README.rst').read(),
    keywords=['async', 'threading', 'multiprocessing'],

    packages=find_packages(),
    scripts=[],
    entry_points={},

    install_requires=[],
    tests_require=[
        'nose',
    ],
    extras_require={},
    include_package_data=True,
    test_suite='nose.collector',

    platforms='any',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent'
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
    ],
)
