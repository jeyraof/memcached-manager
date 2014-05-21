# -*- coding: utf-8 -*-

from pylibmc import Client
from config import MEMCACHE_SERVERS, MEMCACHE_REGEX
from telnetlib import Telnet
import re


def get_pylibmc_client():
    client = Client(servers=(lambda x: [y[0] for y in x])(MEMCACHE_SERVERS),
                    behaviors={
                        'tcp_nodelay': True,
                        'ketama': True
                    },
                    binary=True,
                    )
    return client


def get_telnet_client():
    host = MEMCACHE_SERVERS[0][0]
    port = MEMCACHE_SERVERS[0][1]
    client = Telnet(host=host, port=str(port))

    return client


def get_re_compiler(compiler_type):
    regex = MEMCACHE_REGEX.get(compiler_type, u'')
    if len(regex) > 0:
        return re.compile(regex)

    else:
        return None


def send_cmd_to_telnet(telnet, cmd):
    telnet.write('%s\n' % cmd)
    return telnet.read_until('END')