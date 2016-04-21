#coding:utf-8
from ying.plugins import  BaseAuthentication


class FileAuth(BaseAuthentication):
    def authentication(self, account, passwd):
        '''
        认证方法, 应该返回 True/False
        '''
        user = "test"
        password = "test"
        if user == account and password == passwd:
            return True
        return False

    def authorization(self, account, scope):
        '''
        授权方法, 应该返回 [{"type": repo, "name": image_name, "actions":["pull", "push"]}]
        '''
        repo, ns_img, do_what = scope.split(":")
        namespace = ns_img.split("/")[0]
        if namespace == account:
            # owner
            actions = ["pull", "push"]
        else:
            actions = ["pull"]

        return [{"type": repo, "name": ns_img, "actions": actions}]
