import datetime
from Crypto.Cipher import AES




def encrypt(message, key=None):
    if not key:
        day = datetime.datetime.today().day
        daylen = len(str(day))
        key = str(str(day) + (16 - daylen) * '0').encode('utf-8')
    cipher = AES.new(key, AES.MODE_EAX)
    encrypted_massage, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return encrypted_massage


def decrypt(message, key=None):
    if not key:
        day = datetime.datetime.today().day
        daylen = len(str(day))
        key = str(str(day) + (16 - daylen) * '0').encode('utf-8')
    cipher = AES.new(key, AES.MODE_EAX)
    decrypted_message = cipher.decrypt(message.encode('utf-8'))
    return decrypted_message.decode('utf-8')[:-1]
