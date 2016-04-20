# -*- coding:utf-8 -*-
import os
import imp
from ying import log as logging

log = logging.getLogger(__name__)

def load_url_map(path):
    url_maps = []
    our_dir = path[0]
    for dirpath, dirnames, filenames in os.walk(our_dir):
        for fs in filenames:
            f, f_ext = os.path.splitext(fs)
            if f == '__init__' or f_ext != '.py':
                continue
            fn_, path, desc = imp.find_module(f, [dirpath])
            mod = imp.load_module(f, fn_, path, desc)
            if getattr(mod, 'url_map', None):
                for url, hander in getattr(mod, 'url_map').iteritems():
                    url_maps.append((url, getattr(mod, hander)))
    return url_maps

url_maps = load_url_map(__path__)
log.info('url map:\n'+'\n'.join([ '%s' % _url_map[0] for _url_map in url_maps]))
