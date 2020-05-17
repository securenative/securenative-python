class SecurenativeOptions(object):

    def __init__(self, api_key, api_url, interval, max_events, timeout, auto_send,
                 disable, log_level, fail_over_strategy):
        self.api_key = api_key
        self.api_url = api_url
        self.interval = interval
        self.max_events = max_events
        self.timeout = timeout
        self.auto_send = auto_send
        self.disable = disable
        self.log_level = log_level
        self.fail_over_strategy = fail_over_strategy
