import unittest

from securenative.sn_crypto import encrypt, decrypt


class CryptoTests(unittest.TestCase):
    def test_encrypt_decrypt(self):
        api_key = '6EA4915349C0AAC6F6572DA4F6B00C42'
        data = '{"cid":"198a41ff-a10f-4cda-a2f3-a9ca80c0703b","fp":"6d8cabd95987f8318b1fe01593d5c2a5.24700f9f1986800ab4fcc880530dd0ed"}'
        self.assertEqual(data, decrypt(encrypt(data, api_key), api_key))
