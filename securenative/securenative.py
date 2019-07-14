import json

from securenative.config import _max_allowed_params
from securenative.errors import MissingApiKeyError
from securenative.event_manager import EventManager
from securenative.sdk_options import SecureNativeOptions
from securenative.utils import verify_signature


class SecureNative:
    def __init__(self, api_key, options=SecureNativeOptions()):
        if api_key is None:
            raise MissingApiKeyError()

        self._api_key = api_key
        self._options = options
        self._event_manager = EventManager(self._api_key, self._options)

    def track(self, event):
        _validate_event(event)
        self._event_manager.send_async(event, 'collector/api/v1/track')

    def verify(self, event):
        _validate_event(event)
        response = self._event_manager.send_sync(event, 'collector/api/v1/verify')
        if response.status_code == 200:
            json_result = json.loads(response.text)
            return json_result
        else:
            return None

    def verify_webhook(self, hmac_header, body):
        return verify_signature(self._api_key, body, hmac_header)

    def flush(self):
        self._event_manager.flush()


def _validate_event(event):
    if len(event.params) > _max_allowed_params:
        event.params = event.params[:_max_allowed_params]
