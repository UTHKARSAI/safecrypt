from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

KEY_SIZE = 16  # AES-128

def encrypt_file(file_path, password):
    key = password.encode('utf-8').ljust(KEY_SIZE, b'\0')
    with open(file_path, 'rb') as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    enc_file = file_path + '.enc'
    with open(enc_file, 'wb') as f:
        f.write(cipher.iv + ct_bytes)
    return enc_file

def decrypt_file(enc_file_path, password):
    KEY_SIZE = 16
    key = password.encode('utf-8').ljust(KEY_SIZE, b'\0')
    
    with open(enc_file_path, 'rb') as f:
        file_data = f.read()

    # Check if file length is at least 16 bytes
    if len(file_data) < 16:
        raise ValueError("Encrypted file is too short or corrupted")

    iv = file_data[:16]
    ct = file_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        data = unpad(cipher.decrypt(ct), AES.block_size)
    except ValueError:
        raise ValueError("Incorrect password or corrupted file")

    dec_file = enc_file_path.replace('.enc','')
    with open(dec_file, 'wb') as f:
        f.write(data)
    return dec_file
