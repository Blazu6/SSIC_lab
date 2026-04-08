import os
import time

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

MB = 1024 * 1024

def process_file(input_path, output_path, key, mode='encrypt'):
    buffer_size = 1 * MB
    
    cipher = AES.new(key, AES.MODE_ECB)
        
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        if mode == 'encrypt':
            while True:
                chunk = f_in.read(buffer_size)
                if len(chunk) < buffer_size:
                    f_out.write(cipher.encrypt(pad(chunk, AES.block_size)))
                    break
                else:
                    f_out.write(cipher.encrypt(chunk))
        elif mode == 'decrypt':
            chunk = f_in.read(buffer_size)
            while chunk:
                next_chunk = f_in.read(buffer_size)
                if not next_chunk:
                    decrypted = cipher.decrypt(chunk)
                    f_out.write(unpad(decrypted, AES.block_size))
                    break
                else:
                    f_out.write(cipher.decrypt(chunk))
                    chunk = next_chunk

            

def verify_files(path1, path2):
    if os.path.getsize(path1) != os.path.getsize(path2):
        return False
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        while True:
            b1, b2 = f1.read(1 * MB), f2.read(1 * MB)
            if b1 != b2: return False
            if not b1: return True
  
if __name__ == "__main__":
    files_name = ["TRNG_F.bit", "TRNG_P.bit"]  
    key_sizes = [128, 192, 256]

    for file_name in files_name:
        if not os.path.exists(file_name):
            print(f"Błąd: Nie znaleziono pliku {file_name}!")
            continue 
            
        print(f"\n{'='*50}")
        print(f" ROZPOCZYNAM TESTY DLA PLIKU: {file_name} ")
        print(f"{'='*50}")

        for size in key_sizes:
            print(f"\n--- Wariant: AES-{size} bit ---")
            
            key = os.urandom(size // 8)  

            base_name = file_name.split('.')[0]
            encrypted_file = f"{base_name}_enc_AES{size}.bit"
            decrypted_file = f"{base_name}_dec_AES{size}.bit"

            print(f"Szyfrowanie...")
            start_enc = time.time()
            process_file(file_name, encrypted_file, key, mode='encrypt')
            enc_time = time.time() - start_enc
            
            print("Odszyfrowywanie...")
            start_dec = time.time()
            process_file(encrypted_file, decrypted_file, key, mode='decrypt')
            dec_time = time.time() - start_dec

            # Raport
            print("Wyniki:")
            size_gb = os.path.getsize(file_name) / (1024**3)
            print(f"Rozmiar pliku: {size_gb:.6f} GB") 
            print(f"Czas szyfrowania: {enc_time:.3f} s")
            print(f"Czas deszyfrowania: {dec_time:.3f} s")
            print(f"Średnia prędkość szyfrowania: { (size_gb * 1024) / enc_time:.2f} MB/s")
            print(f"Średnia prędkość deszyfrowania: { (size_gb * 1024) / dec_time:.2f} MB/s")
            
            if verify_files(file_name, decrypted_file):
                print("Weryfikacja: SUKCES (Pliki są identyczne)")
            else:
                print("Weryfikacja: BŁĄD! Coś poszło nie tak.")
            print("===========================")


    

    
    