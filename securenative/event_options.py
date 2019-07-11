import uuid
import time

from securenative.utils import _parse_cookie


class User:
    def __init__(self, user_id=u'', user_email=u'', user_name=u''):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email


class Event:
    def __init__(self, event_type, user=User(), ip=u'127.0.0.1', remote_ip=u'127.0.0.1', user_agent=u'unknown',
                 sn_cookie_value=None, params=None):
        self.event_type = event_type
        self.user = user
        self.remote_ip = remote_ip
        self.ip = ip
        self.user_agent = user_agent
        self.params = params
        if params is None:
            params = list()
        if isinstance(params, list):
            raise ValueError('custom params should be a list of CustomParams, i.e: [CustomParams(key, value), ...])')

        if sn_cookie_value is not None:
            self.cid, self.fp = _parse_cookie(sn_cookie_value)

        self.vid = uuid.uuid1()
        self.ts = time.time() * 1000


class CustomParam:
    def __init__(self, key, value):
        self.key = key
        self.value = value
