import os
import time
import platform
import psutil
import subprocess
from Crypto.Cipher import DES3
from Crypto.Util import Counter

# Zawiera 4 Weak, 12 Semi-Weak oraz 48 Possibly Weak keys
WEAK_KEYS_HEX = {
    # --- WEAK KEYS (4) ---
    "0101010101010101", "FEFEFEFEFEFEFEFE", "E0E0E0E0F1F1F1F1", "1F1F1F1F0E0E0E0E",

    # --- SEMI-WEAK KEYS (12) ---
    "011F011F010E010E", "1F011F010E010E01", "01E001E001F101F1", "E001E001F101F101",
    "01FE01FE01FE01FE", "FE01FE01FE01FE01", "1FE01FE00EF10EF1", "E01FE01FF10EF10E",
    "1FFE1FFE0EFE0EFE", "FE1FFE1FFE0EFE0E", "E0FEE0FEF1FEF1FE", "FEE0FEE0FEF1FEF1",

    # --- POSSIBLY WEAK KEYS (48) ---
    "01011F1F01010E0E", "1F1F01010E0E0101", "E0E01F1FF1F10E0E",
    "0101E0E00101F1F1", "1F1FE0E00E0EF1F1", "E0E0FEFEF1F1FEFE",
    "0101FEFE0101FEFE", "1F1FFEFE0E0EFEFE", "E0FE011FF1FE010E",
    "011F1F01010E0E01", "1FE001FE0EF101FE", "E0FE1F01F1FE0E01",
    "011FE0FE010EF1FE", "1FE0E01F0EF1F10E", "E0FEFEE0F1FEFEF1",
    "011F1FFE010EFEFE", "1FE0FE010EF1FE01", "FE0101FEFE0101FE",
    "01E01FFE01F10EFE", "1FFE01E00EFE01F1", "FE011FE0FE010EF1",
    "FE01E01FFE01F10E", "1FFEE0010EFEF101", "FE1F01E0FE0E01F1",
    "01E0E00101F1F101", "1FFEFE1F0EFEFE0E", "FE1FE001FE0EF101",
    "01E0FE1F01F1FE0E", "E00101E0F10101F1", "FE1F1FFEFE0E0EFE",
    "01FE1FE001FE0EF1", "E0011FFEF1010EFE", "FE011FE0FE010EF1",
    "01FEE01F01FE0EF1", "E001FE1FF101FE0E", "FE01E01FFE01F10E",
    "01FEFE0101FEFE01", "E01F01FEF10E01FE", "FE1FE01FFE0E0EF1",
    "1F01011F0E01010E", "E01F1FE0F10E0EF1", "FEFE0101FEFE0101",
    "1F01E0FE0E01F1FE", "E01FFE01F10EFE01", "FEFE1F1FFEFE0E0E",
    "1F01FEE00E01FEF1", "E0E00101F1F10101", "FEFE0101FEFE0101",
    "1F01FE1F0E01FE0E", "E0E01F1FF1F10E0E", "FEFEE0E0FEFEF1F1"
}

def is_weak(key_part):
    return key_part.hex().upper() in WEAK_KEYS_HEX

def get_safe_3des_key():
    while True:
        raw_key = os.urandom(24)
        key = DES3.adjust_key_parity(raw_key)
        k1, k2, k3 = key[0:8], key[8:16], key[16:24]
        if any(is_weak(part) for part in [k1, k2, k3]):
            continue
        if k1 == k2 or k2 == k3 or k1 == k3:
            continue
        return key

def process_file(input_path, output_path, key, nonce):
    buffer_size = 1024 * 1024 
    ctr = Counter.new(64, initial_value=int.from_bytes(nonce, byteorder='big'))
    cipher = DES3.new(key, DES3.MODE_CTR, counter=ctr)
    
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        while True:
            chunk = f_in.read(buffer_size)
            if not chunk:
                break
            f_out.write(cipher.encrypt(chunk))

def verify_files(path1, path2):
    if os.path.getsize(path1) != os.path.getsize(path2):
        return False
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        while True:
            b1, b2 = f1.read(8192), f2.read(8192)
            if b1 != b2: return False
            if not b1: return True

if __name__ == "__main__":
    # 2. PARAMETRY PLIKÓW
    file_name = "heic1502a.tif"
    encrypted_file = "zaszyfrowany_real.bin"
    decrypted_file = "odszyfrowany_real.tif"
    key_file = "sekretny_klucz.key"

    if not os.path.exists(file_name):
        print(f"BŁĄD: Nie znaleziono pliku {file_name}!")
    else:
        # 3. GENEROWANIE KLUCZA
        print("Generowanie bezpiecznego klucza...")
        key = get_safe_3des_key()
        nonce = os.urandom(8)

        with open(key_file, "wb") as kf:
            kf.write(key)
            kf.write(nonce)

        # 4. SZYFROWANIE
        print(f"Szyfrowanie pliku {file_name}...")
        start_enc = time.time()
        process_file(file_name, encrypted_file, key, nonce)
        enc_time = time.time() - start_enc
        
        # 5. ODSZYFROWYWANIE
        print("Odszyfrowywanie...")
        start_dec = time.time()
        process_file(encrypted_file, decrypted_file, key, nonce)
        dec_time = time.time() - start_dec

        # 6. RAPORT KOŃCOWY
        print("\n=== WYNIKI EKSPERYMENTU ===")
        size_gb = os.path.getsize(file_name) / (1024**3)
        print(f"Rozmiar pliku: {size_gb:.2f} GB")
        print(f"Czas szyfrowania: {enc_time:.3f} s")
        print(f"Czas deszyfrowania: {dec_time:.3f} s")
        print(f"Średnia prędkość: { (size_gb * 1024) / enc_time:.2f} MB/s")
        
        if verify_files(file_name, decrypted_file):
            print("\nWeryfikacja: SUKCES (Pliki są identyczne)")
            print(f"Możesz teraz otworzyć plik: {decrypted_file}")
        else:
            print("\nWeryfikacja: BŁĄD! Coś poszło nie tak.")
        print("===========================")