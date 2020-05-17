from securenative.context.securenative_context import SecureNativeContext


class ContextBuilder(object):

    def __init__(self):
        self.context = SecureNativeContext()

    def with_client_token(self, client_token):
        self.context.client_token = client_token
        return self

    def with_ip(self, ip):
        self.context.ip = ip
        return self

    def with_remote_ip(self, remote_ip):
        self.context.remote_ip = remote_ip
        return self

    def with_headers(self, headers):
        self.context.headers = headers
        return self

    def with_url(self, url):
        self.context.url = url
        return self

    def with_method(self, method):
        self.context.method = method
        return self

    def with_body(self, body):
        self.context.body = body
        return self

    @staticmethod
    def default_context_builder():
        return ContextBuilder()

    def from_http_request(self, request):  # TODO!
        pass

    def build(self):
        return self.context
