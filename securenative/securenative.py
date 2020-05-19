from securenative.api_manager import ApiManager
from securenative.config.configuration_builder import ConfigurationBuilder
from securenative.config.configuration_manager import ConfigurationManager
from securenative.context.context_builder import ContextBuilder
from securenative.event_manager import EventManager
from securenative.exceptions.securenative_config_exception import SecureNativeConfigException
from securenative.exceptions.securenative_sdk_exception import SecureNativeSDKException
from securenative.logger import Logger
from securenative.utils.utils import Utils


class SecureNative:

    def __init__(self, options):
        if Utils.is_null_or_empty(options.api_key):
            raise SecureNativeSDKException("You must pass your SecureNative api key")

        self._options = options
        self._event_manager = EventManager(self._options)

        if self._options.api_url:
            self._event_manager.start_event_persist()

        self._api_manager = ApiManager(self._event_manager, self._options)
        self._securenative = None
        Logger.init_logger(self._options.log_level)

    def init(self, options):
        if self._securenative is None:
            self._securenative = SecureNative(options)
            return self._securenative
        else:
            Logger.debug('This SDK was already initialized.')
            raise SecureNativeSDKException(u'This SDK was already initialized.')

    def init(self, api_key):
        if Utils.is_null_or_empty(api_key):
            raise SecureNativeConfigException("You must pass your SecureNative api key")

        if self._securenative is None:
            builder = ConfigurationBuilder().default_config_builder()
            options = builder.with_api_key(api_key)
            self._securenative = SecureNative(options)
            return self._securenative
        else:
            Logger.debug('This SDK was already initialized.')
            raise SecureNativeSDKException(u'This SDK was already initialized.')

    def init(self):
        options = ConfigurationManager.load_config()
        return self.init(options)

    def get_instance(self):
        return self._securenative

    def get_options(self):
        return self._options

    @staticmethod
    def config_builder():
        return ConfigurationBuilder.default_config_builder()

    @staticmethod
    def context_builder():
        return ContextBuilder.default_context_builder()

    def track(self, event_options):
        self._api_manager.track(event_options)

    def verify(self, event_options):
        self._api_manager.verify(event_options)
