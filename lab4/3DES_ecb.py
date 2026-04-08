from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import os

def encrypt_3des_ecb_random_key(input_file, output_file):
    key = DES3.adjust_key_parity(get_random_bytes(24))
    
    with open("3des_key.txt", "wb") as f:
        f.write(key)
    
    print(f"Wygenerowano losowy klucz: {key.hex()}")

    cipher = DES3.new(key, DES3.MODE_ECB)

    if not os.path.exists(input_file):
        print(f"Błąd: Plik {input_file} nie istnieje!")
        return

    with open(input_file, "rb") as f:
        plaintext = f.read()

    padded_plaintext = pad(plaintext, DES3.block_size)

    ciphertext = cipher.encrypt(padded_plaintext)

    with open(output_file, "wb") as f:
        f.write(ciphertext)

    print(f"Szyfrogram zapisany w: {output_file}")

# --- URUCHOMIENIE ---
# Najpierw stwórz plik z zerami, jeśli go nie masz:
with open("zera.bin", "wb") as f: f.write(b'\x00' * 12500000)

encrypt_3des_ecb_random_key("zera.bin", "3des_ecb_szyfrogram.bin")