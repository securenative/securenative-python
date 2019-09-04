from Crypto.Cipher import AES
from Crypto import Random
from binascii import unhexlify, hexlify

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def encrypt(text, cipherKey):
    iv = Random.new().read(AES.block_size);
    cipher = AES.new(cipherKey, AES.MODE_CBC, iv)
    raw = pad(text)
    return hexlify(iv + cipher.encrypt(raw)).decode('utf-8').strip()


def decrypt(encrypted, cipherKey):
    content = unhexlify(encrypted)
    iv = content[:BLOCK_SIZE]
    cipherText = content[BLOCK_SIZE:]
    aes = AES.new(cipherKey, AES.MODE_CBC, iv)
    return aes.decrypt(cipherText).decode('utf-8').strip()