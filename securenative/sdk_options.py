_securenative_prod = u"https://api.securenative.com"
_securenative_stg = u"https://api.securenative-stg.com"


class SecureNativeOptions:
    def __init__(self, api_url=_securenative_prod, interval=1000, max_events=1000, timeout=1500, auto_send=True,
                 is_sdk_enabled=True, debug_mode=False):
        super().__init__()
        self.timeout = timeout
        self.max_events = max_events
        self.api_url = api_url
        self.interval = interval
        self.auto_send = auto_send
        self.is_sdk_enabled = is_sdk_enabled
        self.debug_mode = debug_mode
