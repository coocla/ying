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

        context = {"user":{"name":"test"}}
        try:
            basic = Basic.split("Basic")[-1].strip()
            passwd = utils.depassword(basic).replace(account,'')[1:].strip()
        except:
            self.set_status(401)
            return self.finish("Auth fail")
        if account == "admin":
            real_pass = nosql.get("registry_credential")
            if not real_pass:
                log.error("No set registry_credential, the credential is admin password to access registry.")
            if passwd != real_pass:
                self.set_status(401)
                return self.finish("Auth fail")
        else:
            auth = db.dauth_get(context, user=account)
            if not auth:
                self.set_status(401)
                return self.finish("Auth fail")
            else:
                if auth.password != passwd:
                    self.set_status(401)
                    return self.finish("Auth fail")
        if scope:
            try:
                repo, ns_img, action = scope.split(":")
                ns, img = ns_img.split("/")
                action = action.split(",")
            except:
                self.set_status(401)
                return self.finish("Auth fail")
            if account == "admin":
                access = [{"type": repo,"name": ns_img, "actions":action}]
            else:
                nslist = [ten["name"] for ten in auth.tenants if ten]
                targetimg = db.docker_image_get(context, ns, img)

                # 计算用户的常用镜像
                hotimage = nosql.get("hot_image_%s" % account) or {}
                if ns_img in hotimage:
                    hotimage[ns_img] += 1
                else:
                    hotimage[ns_img] = 1
                # 保留20个数值
                if len(hotimage) > 20:
                    for i in sorted(hotimage.iteritems(), key=lambda x:x[1])[:len(hotimage)-20]:
                        hotimage.pop(i[0], None)
                nosql.set("hot_image_%s" % account, hotimage)

                if ns in nslist:
                    access = [{"type":repo,"name":ns_img, "actions":action}]
                else:
                    if targetimg:
                        if targetimg.is_private:
                            access = [{"type": repo,"name": ns_img, "actions":[]}]
                        else:
                            access = [{"type": repo,"name": ns_img, "actions":action}]
                    else:
                        access = [{"type": repo,"name": ns_img, "actions":[]}]
        else:
            access = [{"type": repo,"name": "", "actions":[]}]
        self.finish(utils.json_encode({"token": Token(account, access).token}))
