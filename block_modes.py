import typing

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def pad_pkcs7(data_bytes: bytes, block_size: int) -> bytes:
    padding_len = block_size - (len(data_bytes) % block_size)
    if padding_len == 0:
        padding_len = block_size
    return data_bytes + bytes([padding_len] * padding_len)

def unpad_pkcs7(padded: bytes) -> bytes:
    if len(padded) == 0:
        raise ValueError('Invalid padding')
    padding_len = padded[-1]
    if padding_len <= 0 or padding_len > len(padded):
        raise ValueError('Invalid padding')
    if padded[-padding_len:] != bytes([padding_len]) * padding_len:
        raise ValueError('Invalid padding')
    return padded[:-padding_len]

def encrypt_bytes_ecb(data_bytes: bytes, encrypt_block_fn: typing.Callable[[int], int], in_block_size: int = 100, out_block_size: int = 128) -> bytes:
    data_bytes = pad_pkcs7(data_bytes, in_block_size)
    encrypted_data = bytearray()
    for i in range(0, len(data_bytes), in_block_size):
        block = data_bytes[i:i+in_block_size]
        m = int.from_bytes(block, byteorder='big')
        c = encrypt_block_fn(m)
        encrypted_data.extend(c.to_bytes(out_block_size, byteorder='big'))
    return bytes(encrypted_data)

def decrypt_bytes_ecb(encrypted_data_bytes: bytes, decrypt_block_fn: typing.Callable[[int], int], in_block_size: int = 128, out_block_size: int = 100) -> bytes:
    decrypted_data = bytearray()
    for i in range(0, len(encrypted_data_bytes), in_block_size):
        block = encrypted_data_bytes[i:i+in_block_size]
        c = int.from_bytes(block, byteorder='big')
        m = decrypt_block_fn(c)
        decrypted_data.extend(m.to_bytes(out_block_size, byteorder='big'))
    return unpad_pkcs7(bytes(decrypted_data))

def encrypt_bytes_cbc(data_bytes: bytes, encrypt_block_fn: typing.Callable[[int], int], iv: bytes, in_block_size: int = 100, out_block_size: int = 128) -> bytes:
    if len(iv) != in_block_size:
        raise ValueError('IV length must equal in_block_size')
    data_bytes = pad_pkcs7(data_bytes, in_block_size)
    encrypted_data = bytearray()
    prev = iv
    for i in range(0, len(data_bytes), in_block_size):
        block = data_bytes[i:i+in_block_size]
        x = xor_bytes(block, prev)
        m = int.from_bytes(x, byteorder='big')
        c = encrypt_block_fn(m)
        c_bytes = c.to_bytes(out_block_size, byteorder='big')
        encrypted_data.extend(c_bytes)
        prev = c_bytes[:in_block_size]
    return bytes(encrypted_data)

def decrypt_bytes_cbc(encrypted_data_bytes: bytes, decrypt_block_fn: typing.Callable[[int], int], iv: bytes, in_block_size: int = 128, out_block_size: int = 100) -> bytes:
    if len(iv) != out_block_size:
        raise ValueError('IV length must equal out_block_size')
    decrypted_data = bytearray()
    prev = iv
    for i in range(0, len(encrypted_data_bytes), in_block_size):
        block = encrypted_data_bytes[i:i+in_block_size]
        c = int.from_bytes(block, byteorder='big')
        m = decrypt_block_fn(c)
        x = m.to_bytes(out_block_size, byteorder='big')
        original = xor_bytes(x, prev)
        decrypted_data.extend(original)
        prev = block[:out_block_size]
    return unpad_pkcs7(bytes(decrypted_data))
