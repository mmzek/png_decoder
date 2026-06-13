from utils import read_uint32_big_endian_4_bytes

EXPECTED_HEADER_HEX = "89504e470d0a1a0a"

def __check_png_signature(file_path):
    with open(file_path, "rb") as file:
        signature = file.read(8)
        hex_signature = signature.hex()

        if hex_signature != EXPECTED_HEADER_HEX:
            return False
        return True


def __read_ihdr(chunk_data):
    width = read_uint32_big_endian_4_bytes(chunk_data[0:4])
    height = read_uint32_big_endian_4_bytes(chunk_data[4:8])
    bit_depth = chunk_data[8]
    color_type = chunk_data[9]
    compression = chunk_data[10]
    filter_method = chunk_data[11]
    interlace = chunk_data[12]
    print("--- Atrybuty obrazu (IHDR) ---")
    print(f"Szerokość: {width} px")
    print(f"Wysokość: {height} px")
    print(f"Głębia koloru: {bit_depth} bitów")
    print(f"Typ koloru: {color_type}")
    print(f"Metoda kompresji: {compression}")
    print(f"Metoda filtrowania: {filter_method}")
    print(f"Metoda przeplotu: {interlace}")
    print("------------------------------")

def __read_plte(chunk_data):
    if len(chunk_data) % 3 != 0:
        raise ValueError("Długość danych PLTE musi być wielokrotnością 3")
    num_colors = len(chunk_data) // 3
    print(f"PLTE chunk - liczba kolorów: {num_colors}")
    for i in range(num_colors):
        r = chunk_data[i*3]
        g = chunk_data[i*3 + 1]
        b = chunk_data[i*3 + 2]
        print(f"Kolor {i+1}: R={r}, G={g}, B={b}")

def __read_idat(chunk_data):
    print(f"\n[CRITICAL] IDAT (Dane obrazu) - długość: {len(chunk_data)} bajtów")

def __read_iend(chunk_data):
    print(f"\n[CRITICAL] IEND (Koniec pliku)")

def parse_png_chunks(file_path):
    with open(file_path, "rb") as file:
        if not __check_png_signature(file_path):
            print("Plik nie jest poprawnym obrazem PNG.")
            return
        file.seek(8)

        while True:
            length_bytes = file.read(4)
            if not length_bytes:
                break

            chunk_length = read_uint32_big_endian_4_bytes(length_bytes)
            chunk_type = file.read(4).decode('ascii')

            chunk_data = file.read(chunk_length)
            crc = file.read(4)

            if chunk_type == "IHDR":
                __read_ihdr(chunk_data)
            elif chunk_type == "PLTE":
                __read_plte(chunk_data)
            elif chunk_type == "IDAT":
                __read_idat(chunk_data)
            elif chunk_type == "IEND":
                __read_iend(chunk_data)
                break
            else:
               if not chunk_type[0].isupper():
                   print("Ancillary chunks are next")
               else:
                   print("Not known critical chunk")

