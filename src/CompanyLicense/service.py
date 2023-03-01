from config.settings import SECRET_KEY

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import json

key = bytes(SECRET_KEY, "utf-8")

cipher = AES.new(key, AES.MODE_ECB)


def decrypt_string(data):
    data = base64.b64decode(data.encode())
    plaintext = cipher.decrypt(data)
    plaintext = unpad(plaintext, AES.block_size)
    data = json.loads(plaintext.decode())
    return data
