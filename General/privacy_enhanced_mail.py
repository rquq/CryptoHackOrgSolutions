import Crypto
from Crypto.PublicKey import RSA


with open(r'/home/quq/coding/Python/privacy_enhanced_mail_1f696c053d76a78c2c531bb013a92d4a.pem', 'r') as file:
    key = file.read()
    rsa_key = RSA.importKey(key)
    print(rsa_key.d)