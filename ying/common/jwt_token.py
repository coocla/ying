# -*- coding:utf -*-
import jwt
import time
import random
import base64
import hashlib
import datetime
import StringIO
from M2Crypto import X509

from ying.cfg import cfg

class Token(object):
    def __init__(self, account, access):
        self.account =  account
        self.access = access

    @property
    def token(self):
        return self.createToken()

    def createToken(self):
        privateKey = file(cfg.jwt_prikey).read()
        cert = X509.load_cert(cfg.jwt_cert)
        claims = self.claim()
        jose = self.jose_header(cert)

        token = jwt.encode(claims, privateKey, algorithm="RS256", headers=jose)
        return token

    def jose_header(self, cert):
        return {
            "typ":"JWT",
            "alg":"RS256",
            "kid":self.fingerprint(cert)
            }

    def claim(self):
        now = self.timestamp()
        return {
            "iss": cfg.jwt_issuer,
            "sub": self.account,
            "aud": cfg.jwt_service,
            "jti": "".join(str(random.randint(0,9)) for i in xrange(0, 19)),
            "access": self.access,"exp":self.timestamp(cfg.jwt_expire),
            "nbf": now,
            "iat": now
            }

    def timestamp(self, delta=None):
        if delta:
            delta = datetime.datetime.now() + datetime.timedelta(minutes=delta)
            return int(time.mktime(delta.timetuple()))
        return int(time.time())

    def fingerprint(self, cert):
        public = cert.get_pubkey().as_der()
        sig = base64.b32encode(StringIO.StringIO(hashlib.sha256(public).digest()).read(30))
        return self.insert_char_every_n_chars(sig, ':', 4)
        
    def insert_char_every_n_chars(self, string, char=':', every=64):
        return char.join(
                string[i:i + every] for i in xrange(0, len(string), every))
