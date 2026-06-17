import os
from crypto_utils import generate_rsa_keys, build_rsa_from_keys
from png_io import get_combined_idat, save_encrypted_png
from png_processor import (
    process_png_method_a,
    process_png_method_b,
    process_png_decrypt_method_a,
    process_png_decrypt_method_b,
    process_png_cbc_method_a,
    process_png_cbc_method_b,
    process_png_decrypt_cbc_method_a,
    process_png_decrypt_cbc_method_b,
)


def run_demo(base_filepath, output_dir='.'):
    pub_key, priv_key = generate_rsa_keys(bits=1024)
    original_combined_idat = get_combined_idat(base_filepath)

    encrypted_idat_a = process_png_method_a(original_combined_idat, pub_key)
    crypted_path_a = os.path.join(output_dir, 'cryptedapple_method_a.png')
    save_encrypted_png(input_filepath=base_filepath, output_filepath=crypted_path_a, new_idat_chunk=encrypted_idat_a)

    read_encrypted_idat_a = get_combined_idat(crypted_path_a)
    decrypted_idat_a = process_png_decrypt_method_a(read_encrypted_idat_a, priv_key)
    save_encrypted_png(crypted_path_a, os.path.join(output_dir, 'decrypted_apple_method_a.png'), decrypted_idat_a)

    encrypted_idat_b = process_png_method_b(original_combined_idat, pub_key)
    crypted_path_b = os.path.join(output_dir, 'cryptedapple_method_b.png')
    save_encrypted_png(input_filepath=base_filepath, output_filepath=crypted_path_b, new_idat_chunk=encrypted_idat_b)

    read_encrypted_idat_b = get_combined_idat(crypted_path_b)
    decrypted_idat_b = process_png_decrypt_method_b(read_encrypted_idat_b, priv_key)
    save_encrypted_png(crypted_path_b, os.path.join(output_dir, 'decrypted_apple_method_b.png'), decrypted_idat_b)

    iv = os.urandom(100)

    encrypted_idat_cbc_a = process_png_cbc_method_a(original_combined_idat, pub_key, iv)
    crypted_path_cbc_a = os.path.join(output_dir, 'cryptedapple_cbc_method_a.png')
    save_encrypted_png(base_filepath, crypted_path_cbc_a, encrypted_idat_cbc_a)

    read_encrypted_idat_cbc_a = get_combined_idat(crypted_path_cbc_a)
    decrypted_idat_cbc_a = process_png_decrypt_cbc_method_a(read_encrypted_idat_cbc_a, priv_key, iv)
    save_encrypted_png(crypted_path_cbc_a, os.path.join(output_dir, 'decrypted_apple_cbc_method_a.png'), decrypted_idat_cbc_a)

    encrypted_idat_cbc_b = process_png_cbc_method_b(original_combined_idat, pub_key, iv)
    crypted_path_cbc_b = os.path.join(output_dir, 'cryptedapple_cbc_method_b.png')
    save_encrypted_png(base_filepath, crypted_path_cbc_b, encrypted_idat_cbc_b)

    read_encrypted_idat_cbc_b = get_combined_idat(crypted_path_cbc_b)
    decrypted_idat_cbc_b = process_png_decrypt_cbc_method_b(read_encrypted_idat_cbc_b, priv_key, iv)
    save_encrypted_png(crypted_path_cbc_b, os.path.join(output_dir, 'decrypted_apple_cbc_method_b.png'), decrypted_idat_cbc_b)


def build_oaep_demo_keys(pub_key, priv_key):
    e, n = pub_key
    d, _ = priv_key
    lib_key = build_rsa_from_keys(pub_key, priv_key)
    return lib_key

