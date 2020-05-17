class EventOptions(object):

    def __init__(self, event, user_id=None, user_traits=None,
                 securenative_context=None, properties=None, timestamp=None):
        self.event = event
        self.user_id = user_id
        self.user_traits = user_traits
        self.context = securenative_context
        self.properties = properties
        self.timestamp = timestamp
