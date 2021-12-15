from Crypto.Cipher import AES
import os
import base64


class Cipher:
    key_filename = 'key.pem'
    encoding = 'utf-8'

    def __init__(self, key=None):
        if os.path.isfile(self.key_filename):
            self.nonce, self.key = self.load_key()
            self.cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        else:
            # current cipher requires key length of 16 bytes, 1 char = 1 byte if it's ascii char
            keylen = len(key)
            if keylen > 16:
                key = key[:16]
                keylen = len(key)

            self.key = (key + '0' * (16 - keylen)).encode(self.encoding)
            self.cipher = AES.new(self.key, AES.MODE_EAX)
            self.save_key()

    def save_key(self):
        with open(self.key_filename, 'wb') as keyfile:
            [keyfile.write(x) for x in (self.cipher.nonce, self.key)]

    def load_key(self):
        """
        :return: nonce, tag
        """
        with open(self.key_filename, 'rb') as keyfile:
            return [keyfile.read(x) for x in (16, 16)]

    def encrypt(self, message):
        return base64.b64encode(self.cipher.encrypt(message.encode(self.encoding))).decode(self.encoding)

    def decrypt(self, message):
        return self.cipher.decrypt(base64.b64decode(message)).decode(self.encoding)
