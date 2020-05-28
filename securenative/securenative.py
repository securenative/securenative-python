from securenative.api_manager import ApiManager
from securenative.config.configuration_builder import ConfigurationBuilder
from securenative.config.configuration_manager import ConfigurationManager
from securenative.context.context_builder import ContextBuilder
from securenative.event_manager import EventManager
from securenative.exceptions.securenative_config_exception import SecureNativeConfigException
from securenative.exceptions.securenative_sdk_Illegal_state_exception import SecureNativeSDKIllegalStateException
from securenative.exceptions.securenative_sdk_exception import SecureNativeSDKException
from securenative.logger import Logger
from securenative.utils.utils import Utils


class SecureNative:
    _securenative = None

    def __init__(self, options):
        if Utils.is_null_or_empty(options.api_key):
            raise SecureNativeSDKException("You must pass your SecureNative api key")

        self._options = options
        self._event_manager = EventManager(self._options)

        if self._options.api_url:
            self._event_manager.start_event_persist()

        self._api_manager = ApiManager(self._event_manager, self._options)
        Logger.init_logger(self._options.log_level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._event_manager.stop_event_persist()

    @classmethod
    def init_with_options(cls, options):
        if cls._securenative is None:
            cls._securenative = SecureNative(options)
            return cls._securenative
        else:
            Logger.debug('This SDK was already initialized.')
            raise SecureNativeSDKException(u'This SDK was already initialized.')

    @classmethod
    def init_with_api_key(cls, api_key):
        if Utils.is_null_or_empty(api_key):
            raise SecureNativeConfigException("You must pass your SecureNative api key")

        if cls._securenative is None:
            builder = ConfigurationBuilder().default_config_builder()
            options = builder.with_api_key(api_key)
            cls._securenative = SecureNative(options)
            return cls._securenative
        else:
            Logger.debug('This SDK was already initialized.')
            raise SecureNativeSDKException(u'This SDK was already initialized.')

    @classmethod
    def init(cls):
        options = ConfigurationManager.load_config()
        return cls.init_with_options(options)

    @classmethod
    def get_instance(cls):
        if not cls._securenative:
            raise SecureNativeSDKIllegalStateException()
        return cls._securenative

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

    @classmethod
    def _flush(cls):
        cls._securenative = None

    # TODO!
    def verify_request_payload(self, request):
        pass
