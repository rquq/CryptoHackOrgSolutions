from Crypto.PublicKey import RSA
key = RSA.importKey(open(r'/home/quq/coding/Python/2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der', 'rb').read())
print(key.n)