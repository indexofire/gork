# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gork',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A full site project based on feincms.',
    long_description=README.rst,
    url='http://www.gorkproject.com/',
    author='Mark Renton',
    author_email='indexofire@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
