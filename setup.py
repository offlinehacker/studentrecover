# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='studentrecover',
    version='0.1dev',
    description='Asians recovering my student id',
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='web',
    author='Jaka Hudoklin',
    author_email='jakahudoklin@gmail.com',
    url='http://www.github.com/offlinehacker/studentrecover',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'requests',
        'pycurl',
        'antigate'
    ],
    entry_points={
        'console_scripts': [
            'studentrecover = studentrecover:main'
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
