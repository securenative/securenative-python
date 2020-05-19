import copy
import json
import sched
import threading
import time

from securenative.config.securenative_options import SecureNativeOptions
from securenative.exceptions.securenative_http_exception import SecureNativeHttpException
from securenative.http.securenative_http_client import SecureNativeHttpClient
from securenative.logger import Logger


class QueueItem:
    def __init__(self, url, body, retry):
        self.url = url
        self.body = body
        self.retry = retry


class EventManager:
    def __init__(self, options=SecureNativeOptions(), http_client=None):
        if options.api_url is None:
            raise ValueError('API key cannot be None, please get your API key from SecureNative console.')

        if not http_client:
            self.http_client = SecureNativeHttpClient(options)
        else:
            self.http_client = http_client

        self.options = options
        self.queue = list()
        self.send_enabled = False
        self.attempt = 0
        self.coefficients = [1, 1, 2, 3, 5, 8, 13]
        self.scheduler = None

        if self.options.auto_send and not self.options.disable:
            interval_seconds = max(options.interval // 1000, 1)
            threading.Timer(interval_seconds, self.flush).start()

    def send_async(self, event, resource_path):
        if self.options.disable:
            Logger.warning("SDK is disabled. no operation will be performed")
            return

        item = QueueItem(
            resource_path,
            json.dumps(event.as_dict()),
            False
        )

        self.queue.insert(0, item)
        if self._is_queue_full():
            self.queue = self.queue[:len(self.queue - 1)]

    def flush(self):
        queue_copy = copy.copy(self.queue)
        self.queue = list()

        for item in queue_copy:
            self.http_client.post(item.url, item.body)

    def send_sync(self, event, resource_path, retry):
        if self.options.disable:
            Logger.warning("SDK is disabled. no operation will be performed")
            return

        Logger.debug("Attempting to send event {}".format(event.as_dict()))
        res = self.http_client.post(
            resource_path,
            json.dumps(event.as_dict())
        )
        if res.status != 200:
            Logger.info("SecureNative failed to call endpoint {} with event {}. adding back to queue")

            item = QueueItem(
                resource_path,
                json.dumps(event.as_dict()),
                retry
            )
            self.queue.insert(0, item)
            if self._is_queue_full():
                self.queue = self.queue[:len(self.queue - 1)]

    def _is_queue_full(self):
        return len(self.queue) > self.options.max_events

    def _send_events(self):
        if len(self.queue) > 0 and self.send_enabled:
            for item in self.queue:
                try:
                    res = self.http_client.post(item.url, item.body)
                    if res.status is 401:
                        item.retry = False
                    elif res.status != 200:
                        raise SecureNativeHttpException(res.status)

                    Logger.debug("Event successfully sent; {}".format(item.body))
                    self.queue.remove(item)
                except Exception as e:
                    Logger.error("Failed to send event; {}".format(e))
                    if item.retry:
                        if len(self.coefficients) == self.attempt + 1:
                            self.attempt = 0

                        back_off = self.coefficients[self.attempt] * self.options.interval
                        Logger.debug("Automatic back-off of {}".format(back_off))
                        self.send_enabled = False
                        time.sleep(back_off)
                        self.send_enabled = True
                    else:
                        self.queue.remove(item)

    def start_event_persist(self):
        Logger.debug("Starting automatic event persistence")
        if self.options.auto_send or self.send_enabled:
            self.send_enabled = True
            try:
                self.scheduler = sched.scheduler(time.time, time.sleep)
                self.scheduler.enter(self.options.interval, 1, self._send_events)
                self.scheduler.run()
            except Exception:
                pass
        else:
            Logger.debug("Automatic event persistence is disabled, you should persist events manually")

    def stop_event_persist(self):
        if self.send_enabled:
            Logger.debug("Attempting to stop automatic event persistence")
            try:
                self.scheduler.cancel(self._send_events)
            except ValueError:
                pass

            Logger.debug("Stopped event persistence")
