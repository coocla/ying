# -*- coding:utf-8 -*-
import os
import sys
import logging
import logging.handlers

from odc_api.cfg import cfg

def create_logger(name, filename):
    root = logging.getLogger(name)
    FORMAT = '[%(levelname)-8s] [%(asctime)s] [%(name)s:%(lineno)d] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    channel = logging.handlers.RotatingFileHandler(
            filename=filename,
            maxBytes=100000000,
            backupCount=10)
    channel.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    root.addHandler(channel)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    root.addHandler(console)

    root.setLevel(getattr(logging, cfg.log_level.upper(), logging.DEBUG))
    return logging.getLogger(name)

loggers = {}

def getLogger(name):
    if name not in loggers:
        if not os.path.isdir(cfg.log_dir):
            os.makedirs(cfg.log_dir)
        loggers[name] = create_logger(name, os.path.join(cfg.log_dir, cfg.log_file))
    return loggers[name]
