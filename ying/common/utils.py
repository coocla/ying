# -*- coding:utf-8 -*-
import os
import sys
import imp
import json
import datetime
import traceback

from tornado import escape

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, obj)

def json_encode(value):
    """Python object to JSON"""
    return json.dumps(value, cls=ComplexEncoder).replace("</", "<\\/")

def json_decode(value):
    """JSON to Python object"""
    return escape.json_decode(value)

def depassword(password):
    return base64_decode(password)

def import_class(import_str):
    mod_str, _sep, class_str = import_str.rpartition('.')
    try:
        __import__(mod_str)
        return getattr(sys.modules[mod_str], class_str)
    except (ValueError, AttributeError):
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str, traceback.print_exc()))

def import_module(import_path):
    module_name = os.path.basename(import_path)
    module_path = os.path.dirname(import_path)
    try:
        fn_, path, desc = imp.find_module(module_name, [module_path])
        mod = imp.load_module(module_name, fn_, path, desc)
    except:
        raise ImportError('Module %s cannot be found (%s)' %
                         (import_path, traceback.print_exc()))
    return mod
