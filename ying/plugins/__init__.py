#coding:utf-8
from ying.cfg import cfg
from ying.common import utils

class BaseAuthentication(object):
    def authentication(self):
        raise NotImplementedError(".authentication() must be overridden.")

    def authorization(self):
        raise NotImplementedError(".authorization() must be overridden.")


def auth_driver():
    cls = utils.import_class(cfg.auth_driver)
    return cls
