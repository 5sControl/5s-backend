from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

from config.settings import SECRET_KEY

key = bytes(SECRET_KEY, "utf-8")


def encrypt(data):
    cipher = AES.new(key, AES.MODE_ECB)
    data = pad(data.encode(), AES.block_size)
    ciphertext = cipher.encrypt(data)
    return base64.b64encode(ciphertext).decode()


def decrypt(data):
    cipher = AES.new(key, AES.MODE_ECB)
    data = base64.b64decode(data.encode())
    plaintext = cipher.decrypt(data)
    plaintext = unpad(plaintext, AES.block_size)
    return plaintext.decode()


def is_encrypted(password):
    return password[-2:] == "=="
