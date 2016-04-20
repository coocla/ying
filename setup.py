# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

def requires():
    with open('requirements.txt') as fp:
        return fp.readlines()

def version():
    with open('ying/versions.txt') as fp:
        return fp.read().strip()
setup(
    name="ying",
    version="1",
    author="coocla",
    install_requires=requires(),
    scripts=[
        "bin/ying_api",
    ],

    packages=find_packages(),
    data_files=[
        ('/etc/ying/', ['etc/ying.conf']),
    ],
)
