import json
import unittest


from securenative.http.securenative_http_client import SecureNativeHttpClient

from securenative.utils.version_utils import VersionUtils


class HttpClientTests(unittest.TestCase):
    def test_post(self):
        client = SecureNativeHttpClient()
        api_key = u'ABC'
        request_body = {"key": "test1", "value": "test2"}
        response = client.post(path=u"https://httpbin.org/post", body=json.dumps(request_body))

        self.assertEqual(response.status_code, 200)
        json_body = json.loads(response.text)
        self.assertEqual(json_body['headers']['Content-Type'], 'application/json')
        self.assertEqual(json_body['headers']['User-Agent'], 'SecureNative-python')
        self.assertEqual(json_body['headers']['Sn-Version'], VersionUtils.get_version())
        self.assertEqual(json_body['headers']['Authorization'], api_key)
        self.assertEqual(json_body['json'], request_body)
