from utils import read_uint32_big_endian_4_bytes


def anonymize_png(input_path, output_path):
    with open(input_path, "rb") as source, open(output_path, "wb") as result:
        KNOWN_CRITICAL_CHUNKS = {"IHDR", "PLTE", "IDAT", "IEND"}

        signature = source.read(8)
        result.write(signature)

        while True:
            length_bytes = source.read(4)
            if not length_bytes:
                break
            chunk_length = read_uint32_big_endian_4_bytes(length_bytes)
            chunk_type = source.read(4).decode("ascii")
            chunk_data = source.read(chunk_length)
            crc = source.read(4)

            is_critical = chunk_type[0].isupper()

            if is_critical and chunk_type in KNOWN_CRITICAL_CHUNKS:
                result.write(length_bytes)
                result.write(chunk_type.encode("ascii"))
                result.write(chunk_data)
                result.write(crc)
            if chunk_type == "IEND":
                break