class RequestUtils(object):
    SECURENATIVE_COOKIE = "_sn"
    SECURENATIVE_HEADER = "x-securenative"

    @staticmethod
    def get_secure_header_from_request(headers):
        try:
            return headers[RequestUtils.SECURENATIVE_HEADER]
        except Exception:
            return ""

    @staticmethod
    def get_client_ip_from_request(request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        except Exception:
            return ""

    @staticmethod
    def get_remote_ip_from_request(request):
        try:
            return request.raw._original_response.fp.raw._sock.getpeername()[0]
        except Exception:
            return ""
