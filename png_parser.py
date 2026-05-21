import struct
import zlib

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def parse_png(filepath):
    with open(filepath, "rb") as f:

        #checking if file is png
        signature = f.read(8)
        if signature != PNG_SIGNATURE:
            print("This is not a PNG file")
            return

        print("This is a PNG file\n")

        count_IDAT_chunks = 0
        count_IDAT_chunks_length = 0

        #reading chunks in a loop
        while True:
            length_bytes = f.read(4)
            if len(length_bytes) < 4:
                break
            #unpack to int
            length = struct.unpack('>I', length_bytes)[0]
            type_bytes = f.read(4)
            chunk_type = type_bytes.decode('ascii')
            data = f.read(length)
            crc = struct.unpack('>I', f.read(4))[0]

            print(f"Chunk: {chunk_type}, Length: {length}, CRC: {crc:#010x}")

            #reading IHDR data
            if chunk_type == 'IHDR':
                width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack('>IIBBBBB', data)
                print("This is IHDR data:")
                print(f"  Width: {width}, Height: {height}")
                print(f"  Bit depth: {bit_depth}, Color type: {color_type}")
                print(f"  Compression: {compression}, Filter: {filter_method}, Interlace: {interlace}\n ")

            #reading PLTE chunk
            if chunk_type == 'PLTE':
                colors = [data[i:i + 3] for i in range(0, len(data), 3)]
                print(f"  Palette: {len(colors)} colors")

            # counting IDAT chunks and their length
            if chunk_type == 'IDAT':
                count_IDAT_chunks += 1
                count_IDAT_chunks_length += length

            #verifying CRC using zlib "& 0xFFFFFFFF" ensures it is an unsigned 32-bit number
            computed_crc = zlib.crc32(type_bytes + data) & 0xFFFFFFFF
            if crc != computed_crc:
                print(f"  WARNING: CRC mismatch!")

            if chunk_type == 'IEND':
                break

        print(f"\nCounted: {count_IDAT_chunks} IDAT chunks, {count_IDAT_chunks_length} bytes total")
