import uuid
import time

from securenative.utils.utils import _parse_cookie


class User:
    def __init__(self, user_id=u'', user_email=u'', user_name=u''):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email


class Event:
    def __init__(self, event_type, user=User(), ip=u'127.0.0.1', remote_ip=u'127.0.0.1', user_agent=u'unknown',
                 sn_cookie_value=None, params={}):
        self.event_type = event_type
        self.user = user
        self.remote_ip = remote_ip
        self.ip = ip
        self.user_agent = user_agent
        self.params = params
        self.cid = ''
        self.fp = ''

        if self.params is None:
            self.params = {}

        if sn_cookie_value is not None:
            self.cid, self.fp = _parse_cookie(sn_cookie_value)

        self.vid = str(uuid.uuid4())
        self.ts = int(time.time()) * 1000

    def as_dict(self):
        return {
            "eventType": self.event_type,
            "user": {
                "id": self.user.user_id,
                "email": self.user.user_email,
                "name": self.user.user_name
            },
            "remoteIP": self.remote_ip,
            "ip": self.ip,
            "cid": self.cid,
            "fp": self.fp,
            "ts": self.ts,
            "vid": self.vid,
            "userAgent": self.user_agent,
            "device": {},
            "params": self.params
        }
