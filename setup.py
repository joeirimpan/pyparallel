#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'requests',
    'Click'
]

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest'
]

setup(
    name='split-downloader',
    version='0.2.1',
    description="Parallel downloader",
    long_description=readme,
    author="Joe Paul",
    author_email='joeirimpan@gmail.com',
    url='https://github.com/joeirimpan/pyparallel',
    packages=find_packages(include=['pyparallel']),
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        download=pyparallel:cli
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
    long_description_content_type='text/markdown',
    setup_requires=setup_requirements,
)
