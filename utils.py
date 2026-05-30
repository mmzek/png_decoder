def read_uint32_big_endian_4_bytes(bytes_data):
    if len(bytes_data) != 4:
         raise ValueError("4 bytes only")

    value = (bytes_data[0] << 24) | (bytes_data[1] << 16) | (bytes_data[2] << 8) | bytes_data[3]

    return value