import struct
import binascii

def get_combined_idat(filepath):
    combined_idat_data = bytearray()
    with open(filepath, 'rb') as file:
        signature = file.read(8)
        while True:
            length_bytes = file.read(4)
            if not length_bytes:
                break
            chunk_length = struct.unpack(">I", length_bytes)[0]
            chunk_type = file.read(4).decode('ascii')
            chunk_data = file.read(chunk_length)
            chunk_crc = file.read(4)
            if chunk_type == 'IDAT':
                combined_idat_data.extend(chunk_data)
            elif chunk_type == 'IEND':
                break
    return bytes(combined_idat_data)

def create_png_chunk(chunk_type, chunk_data):
    type_bytes = chunk_type.encode('ascii')
    crc = binascii.crc32(type_bytes + chunk_data)
    length_bytes = struct.pack('>I', len(chunk_data))
    crc_bytes = struct.pack('>I', crc)
    return length_bytes + type_bytes + chunk_data + crc_bytes

def save_encrypted_png(input_filepath, output_filepath, new_idat_chunk):
    with open(input_filepath, 'rb') as infile, open(output_filepath, 'wb') as outfile:
        signature = infile.read(8)
        outfile.write(signature)
        idat_written = False
        while True:
            length_bytes = infile.read(4)
            if not length_bytes:
                break
            chunk_length = struct.unpack('>I', length_bytes)[0]
            chunk_type_bytes = infile.read(4)
            chunk_type = chunk_type_bytes.decode('ascii')
            chunk_data = infile.read(chunk_length)
            chunk_crc = infile.read(4)
            original_chunk = length_bytes + chunk_type_bytes + chunk_data + chunk_crc
            if chunk_type == 'IDAT':
                if not idat_written:
                    outfile.write(new_idat_chunk)
                    idat_written = True
            else:
                outfile.write(original_chunk)
            if chunk_type == 'IEND':
                break

