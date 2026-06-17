import math
from Crypto.Util.number import getPrime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def nwd(a,b):
    while b != 0:
        a,b = b, a % b
    return a

def find_e(phi_n):
    e = 3
    while nwd(e ,phi_n) != 1:
        e+= 2
    return e

def generate_rsa_keys(bits=1024):
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    n = p * q
    phi_n = (p-1) * (q-1)
    e = find_e(phi_n)
    d = pow(e, -1, phi_n)
    public_key = (e,n)
    private_key = (d,n)
    return public_key, private_key

def encrypt_rsa(message, public_key):
    e, n = public_key
    c = pow(message,e,n)
    return c

def decrypt_rsa(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext,d,n)
    return m

def oaep_encrypt(data, pub_key):
    e, n = pub_key
    d, _ = None, None
    return None

def build_rsa_from_keys(pub_key, priv_key=None):
    e, n = pub_key
    if priv_key is None:
        return RSA.construct((n, e))
    d, _ = priv_key
    return RSA.construct((n, e, d))

def oaep_cipher_from_keys(pub_key, priv_key=None):
    key = build_rsa_from_keys(pub_key, priv_key)
    return PKCS1_OAEP.new(key)

