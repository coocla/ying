# -*- coding:utf-8 -*-
import os
from tornado.options import define, options, parse_config_file, parse_command_line

CFG = [
    {
        "name": "config",
        "default": "/etc/ying/ying.conf",
        "type": str,
        "callback": lambda p: parse_config_file(p, final=False),
        "help": "API config file",
    },
    {
        "name": "address",
        "default": "0.0.0.0",
        "type": str,
        "help": "API listen address",
    },
    {
        "name": "port",
        "default": 8337,
        "type": int,
        "help": "API listen port",
    },
    {
        "name": "log_level",
        "default": "debug",
        "type": str,
        "metavar": "debug|info|warning|error",
        "help": "Log level for api (e.g. debug)",
    },
    {
        "name": "log_file",
        "default": "ying.log",
        "type": str,
        "metavar": "ying",
        "help": "process log file",
    },
    {
        "name": "log_dir",
        "default": "/var/log/ying",
        "type": str,
        "metavar": "PATH",
        "help": "If non-empty, write log files in this directory",
    },
    {
        "name": "jwt_prikey",
        "default": "/etc/ying/registry_auth.key",
        "type": str,
        "help": "Docker Registry v2 Token private key"
    },
    {
        "name": "jwt_cert",
        "default": "/etc/ying/registry_auth.crt",
        "type": str,
        "help": "Docker Registry v2 Token cert"
    },
    {
        "name": "jwt_issuer",
        "default": "Auth",
        "type": str,
        "help": "Docker Registry v2 Auth issuer, JWT field: iss"
    },
    {
        "name": "jwt_service",
        "default": "RegistryAuthServer",
        "type": str,
        "help": "Docker Registry v2 Auth service, JWT field: aud"
    },
    {
        "name": "jwt_expire",
        "default": 5,
        "type": int, 
        "help": "JWT Token expire, unite minutes"
    },
    {
        "name": "auth_driver",
        "default": "ying.plugins.FileAuthentication.FileAuth",
        "type": str,
        "help": "Docker Registry account authentication plugin"
    },
]


def register(opts):
    for opt in opts:
        if opt.has_key("name"):
            options._options.pop(opt["name"], None)
            define(opt.pop("name"), **opt)
    if hasattr(options, "config") and os.path.isfile(options.config):
        parse_config_file(options.config)
        parse_command_line()
    return options

cfg = register(CFG)
