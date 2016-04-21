# -*- coding:utf-8 -*-
import tornado.web

from ying.cfg import cfg
from ying import log as logging
from ying.common import utils
from ying.common.jwt_token import Token
from ying.plugins import auth_driver


url_map = {
    r"/auth/?$": "TokenAuthServer",
}

log = logging.getLogger(__name__)

class TokenAuthServer(tornado.web.RequestHandler):
    def get(self):
        '''
        Docker Registry v2 token auth api
        '''
        service = self.get_argument("service", None)
        scope = self.get_argument("scope", None)
        account = self.get_argument("account", None)
        Basic = self.request.headers.get("Authorization", None)

        try:
            basic = Basic.split("Basic")[-1].strip()
            passwd = utils.depassword(basic).replace(account,'')[1:].strip()
        except:
            self.set_status(401)
            return self.finish("Auth fail")
        if not auth_driver.authentication(account, passwd):
            log.warn("user % auth failed" % account)
            self.set_status(401)
            return self.finish("Auth fail")
        access = auth_driver.authorization(account, scope)
        self.finish(utils.json_encode({"token": Token(account, access).token}))
