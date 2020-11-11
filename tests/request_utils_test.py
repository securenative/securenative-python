import unittest

import requests_mock

from securenative.config.securenative_options import SecureNativeOptions
from securenative.utils.request_utils import RequestUtils


class RequestUtilsTest(unittest.TestCase):

    def test_proxy_headers_extraction_from_request_ipv4(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "203.0.113.1"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("203.0.113.1", client_ip)

    def test_proxy_headers_extraction_from_request_ipv6(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "6559:6335:f572:14c6:4198:dd09:ddea:04f4"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("6559:6335:f572:14c6:4198:dd09:ddea:04f4", client_ip)

    def test_proxy_headers_extraction_from_request_multiple_ips(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_HTTP_X_FORWARDED_FOR_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "HTTP_X_FORWARDED_FOR": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_HTTP_X_FORWARDED_FOR_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "HTTP_X_FORWARDED_FOR": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_X_FORWARDED_FOR_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "X_FORWARDED_FOR": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_X_FORWARDED_FOR_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "X_FORWARDED_FOR": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_REMOTE_ADDR_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "REMOTE_ADDR": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_REMOTE_ADDR_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "REMOTE_ADDR": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded-for": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_for_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded-for": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_client_ip_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-client-ip": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_client_ip_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-client-ip": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_real_ip_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-real-ip": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_real_ip_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-real-ip": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_forwarded_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_cluster_client_ip_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-cluster-client-ip": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_x_cluster_client_ip_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-client-ip": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded-for": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_for_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded-for": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_forwarded_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "forwarded": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_via_for_header_single_ip(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "via": "141.246.115.116"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_from_via_header_multiple_ips(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "via": "141.246.115.116, 203.0.113.1, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("141.246.115.116", client_ip)

    def test_extraction_priority_with_x_forwarded_for(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-forwarded-for": "203.0.113.1",
                "x-real-ip": "198.51.100.101",
                "x-client-ip": "198.51.100.102"
            }

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("203.0.113.1", client_ip)

    def test_extraction_priority_without_x_forwarded_for(self):
        options = SecureNativeOptions()

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "x-real-ip": "198.51.100.101",
                "x-client-ip": "203.0.113.1, 141.246.115.116, 12.34.56.3"}

        client_ip = RequestUtils.get_client_ip_from_request(request, options)

        self.assertEqual("203.0.113.1", client_ip)
