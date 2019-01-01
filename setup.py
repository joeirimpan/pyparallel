#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'Click'
]

setup_requirements = [
    # TODO(joeirimpan): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='split-downloader',
    version='0.1.0',
    description="Parallel downloader",
    long_description=readme + '\n\n' + history,
    author="Joe Paul",
    author_email='joeirimpan@gmail.com',
    url='https://github.com/joeirimpan/pyparallel',
    packages=find_packages(include=['pyparallel']),
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        download=manage:cli
    ''',
    license="MIT license",
    zip_safe=False,
    keywords='pyparallel',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
