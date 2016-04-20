#coding:utf-8
def VERSION():
    with open('versions.txt') as fp:
        return fp.read().strip()
