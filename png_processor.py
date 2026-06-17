import zlib
from crypto_utils import encrypt_rsa, decrypt_rsa
from block_modes import (
    encrypt_bytes_ecb as encrypt_ecb_generic,
    decrypt_bytes_ecb as decrypt_ecb_generic,
    encrypt_bytes_cbc as encrypt_cbc_generic,
    decrypt_bytes_cbc as decrypt_cbc_generic,
)
from png_io import create_png_chunk


def process_png_method_a(idat_compressed_bytes, pub_key):
    raw = zlib.decompress(idat_compressed_bytes)
    encrypted = encrypt_ecb_generic(raw, lambda m: encrypt_rsa(m, pub_key))
    recompressed_data = zlib.compress(encrypted)
    return create_png_chunk('IDAT', recompressed_data)


def process_png_method_b(idat_compressed_bytes, pub_key):
    encrypted = encrypt_ecb_generic(idat_compressed_bytes, lambda m: encrypt_rsa(m, pub_key))
    return create_png_chunk('IDAT', encrypted)


def process_png_decrypt_method_a(encrypted_idat_bytes, priv_key):
    encrypted = zlib.decompress(encrypted_idat_bytes)
    raw = decrypt_ecb_generic(encrypted, lambda c: decrypt_rsa(c, priv_key))
    recompressed_data = zlib.compress(raw)
    return create_png_chunk('IDAT', recompressed_data)


def process_png_decrypt_method_b(encrypted_idat_bytes, priv_key):
    decrypted_compressed_data = decrypt_ecb_generic(encrypted_idat_bytes, lambda c: decrypt_rsa(c, priv_key))
    return create_png_chunk('IDAT', decrypted_compressed_data)


def process_png_cbc_method_a(idat_compressed_bytes, pub_key, iv):
    raw = zlib.decompress(idat_compressed_bytes)
    encrypted = encrypt_cbc_generic(raw, lambda m: encrypt_rsa(m, pub_key), iv)
    recompressed_data = zlib.compress(encrypted)
    return create_png_chunk('IDAT', recompressed_data)


def process_png_decrypt_cbc_method_a(encrypted_idat_bytes, priv_key, iv):
    encrypted = zlib.decompress(encrypted_idat_bytes)
    raw = decrypt_cbc_generic(encrypted, lambda c: decrypt_rsa(c, priv_key), iv)
    recompressed_data = zlib.compress(raw)
    return create_png_chunk('IDAT', recompressed_data)


def process_png_cbc_method_b(idat_compressed_bytes, pub_key, iv):
    encrypted = encrypt_cbc_generic(idat_compressed_bytes, lambda m: encrypt_rsa(m, pub_key), iv)
    return create_png_chunk('IDAT', encrypted)


def process_png_decrypt_cbc_method_b(encrypted_idat_bytes, priv_key, iv):
    decrypted = decrypt_cbc_generic(encrypted_idat_bytes, lambda c: decrypt_rsa(c, priv_key), iv)
    return create_png_chunk('IDAT', decrypted)

