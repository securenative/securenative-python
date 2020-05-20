import os
from configparser import ConfigParser, NoSectionError

from securenative.config.configuration_builder import ConfigurationBuilder


class ConfigurationManager(object):
    DEFAULT_CONFIG_FILE = "securenative.ini"
    CUSTOM_CONFIG_FILE_ENV_NAME = "SECURENATIVE_COMFIG_FILE"
    config = ConfigParser()

    @classmethod
    def read_resource_file(cls, resource_path):
        cls.config.read(resource_path)
        sections = cls.config.sections()

        properties = {}
        for section in sections:
            options = cls.config.options(section)
            for option in options:
                try:
                    properties[option] = cls.config.get(section, option)
                except NoSectionError:
                    properties[option] = None

        return properties

    @classmethod
    def _get_resource_path(cls, env_name):
        env_value = os.environ.get(env_name)

        if env_value:
            return env_value

        return os.environ.get(cls.DEFAULT_CONFIG_FILE)

    @staticmethod
    def config_builder():
        return ConfigurationBuilder.default_config_builder()

    @classmethod
    def _get_env_or_default(cls, properties, key, default):
        if properties[key]:
            return properties[key]
        return default

    @classmethod
    def load_config(cls):
        builder = ConfigurationBuilder()
        options = builder.get_default_securenative_options()
        resource_path = cls._get_env_or_default(cls.DEFAULT_CONFIG_FILE, cls.CUSTOM_CONFIG_FILE_ENV_NAME)
        properties = cls.read_resource_file(resource_path)

        builder.\
            with_api_key(cls._get_env_or_default(properties, "SECURENATIVE_API_KEY", options.api)).\
            with_api_url(cls._get_env_or_default(properties, "SECURENATIVE_API_URL", options.api_url)).\
            with_interval(cls._get_env_or_default(properties, "SECURENATIVE_INTERVAL", options.interval)).\
            with_max_events(cls._get_env_or_default(properties, "SECURENATIVE_MAX_EVENTS", options.max_events)).\
            with_timeout(cls._get_env_or_default(properties, "SECURENATIVE_TIMEOUT", options.timeout)).\
            with_auto_send(cls._get_env_or_default(properties, "SECURENATIVE_AUTO_SEND", options.auto_send)).\
            with_disable(cls._get_env_or_default(properties, "SECURENATIVE_DISABLE", options.disable)).\
            with_log_level(cls._get_env_or_default(properties, "SECURENATIVE_LOG_LEVEL", options.log_level)).\
            with_fail_over_strategy(cls._get_env_or_default(properties, "SECURENATIVE_FAILOVER_STRATEGY", options))
