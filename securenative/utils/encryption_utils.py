from securenative.models.client_token import ClientToken
from Crypto.Cipher import AES
from Crypto import Random
from binascii import unhexlify, hexlify


class EncryptionUtils(object):
    BLOCK_SIZE = 16

    @classmethod
    def encrypt(cls, text, cipher_key):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
        raw = cls._pad(text)
        return hexlify(iv + cipher.encrypt(raw)).decode('utf-8').strip()

    @classmethod
    def decrypt(cls, encrypted, cipher_key):
        content = unhexlify(encrypted)
        iv = content[:cls.BLOCK_SIZE]
        cipher_text = content[cls.BLOCK_SIZE:]
        aes = AES.new(cipher_key, AES.MODE_CBC, iv)
        cid, vid, fp = aes.decrypt(cipher_text).decode('utf-8').strip()
        return ClientToken(cid, vid, fp)

    @classmethod
    def _pad(cls, s):
        return s + (cls.BLOCK_SIZE - len(s) % cls.BLOCK_SIZE) * chr(cls.BLOCK_SIZE - len(s) % cls.BLOCK_SIZE)

