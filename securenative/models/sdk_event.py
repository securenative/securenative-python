import uuid

from securenative.context.context_builder import ContextBuilder
from securenative.models.request_context import RequestContextBuilder
from securenative.utils.date_utils import DateUtils
from securenative.utils.encryption_utils import EncryptionUtils


class SDKEvent(object):

    def __init__(self, event_options, securenative_options):
        if event_options.securenative_context:
            context = event_options.securenative_context
        else:
            context = ContextBuilder.default_context_builder().build()

        client_token = EncryptionUtils.decrypt(context.client_token, securenative_options.api_key)

        self.rid = uuid.uuid4()
        self.event_optionsType = event_options.getevent_options()
        self.userId = event_options.getUserId()
        self.userTraits = event_options.getUserTraits()
        self.request = RequestContextBuilder().\
            with_cid(client_token.cid)\
            .with_vid(client_token.vid)\
            .with_fp(client_token.fp)\
            .with_ip(context.ip)\
            .with_remote_ip(context.remote_ip)\
            .with_method(context.method)\
            .with_url(context.url)\
            .with_headers(context.headers)\
            .build()

        self.timestamp = DateUtils.to_timestamp(event_options.timestamp)
        self.properties = event_options.getProperties()
