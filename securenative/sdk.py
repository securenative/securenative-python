import json

from securenative.config import _max_allowed_params
from securenative.event_manager import EventManager
from securenative.logger import sn_logging
from securenative.sdk_options import SecureNativeOptions
from securenative.utils.utils import verify_signature


class SecureNative:
    def __init__(self, api_key, options=SecureNativeOptions()):
        if api_key is None:
            raise ValueError('API key cannot be None, please get your API key from SecureNative console.')

        self._api_key = api_key
        self._options = options
        self._event_manager = EventManager(self._api_key, self._options)
        if self._options and self._options.debug_mode:
            enable_sn_logging = self._options.debug_mode
            sn_logging("sn logging was activated")

    def track(self, event):
        sn_logging("Track event call")
        if not self._options.is_sdk_enabled:
            return
        _validate_event(event)
        self._event_manager.send_async(event, 'collector/api/v1/track')

    def verify(self, event):
        sn_logging("Verify event call")
        if not self._options.is_sdk_enabled:
            return _default_verify_result()
        _validate_event(event)

        try:
            response = self._event_manager.send_sync(event, 'collector/api/v1/verify')

            if response.status_code == 200:
                json_result = json.loads(response.text)
                return json_result
            else:
                return _default_verify_result()

        except Exception:
            return _default_verify_result

    def verify_webhook(self, hmac_header, body):
        sn_logging("Verify webhook was called")
        return verify_signature(self._api_key, body, hmac_header)

    def flush(self):
        self._event_manager.flush()


def _default_verify_result():
    result = dict()
    result['riskLevel'] = u'low'
    result['score'] = 0
    result['triggers'] = []
    return result


def _validate_event(event):
    if event.params is not None:
        if len(event.params) > _max_allowed_params:
            event.params = event.params[:_max_allowed_params]
