import os
import time
from Crypto.Cipher import AES
from Crypto.Util import Counter

def process_aes_cfb(input_path, output_path, key, iv, mode='encrypt'):
    # Bufor 2MB 
    buffer_size = 2 * 1024 * 1024
    
    if mode == 'encrypt':
        cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    else:
        cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
        
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        while True:
            chunk = f_in.read(buffer_size)
            if not chunk:
                break
            if mode == 'encrypt':
                f_out.write(cipher.encrypt(chunk))
            else:
                f_out.write(cipher.decrypt(chunk))

def run_experiment(file_path, key_size):
    print(f"\n--- TEST: AES-{key_size} bit ---")
    key = os.urandom(key_size // 8)
    iv = os.urandom(16)
    
    enc_file = f"enc_{key_size}.bin"
    dec_file = f"dec_{key_size}.mp4"
    
    # Szyfrowanie
    start = time.time()
    process_aes_cfb(file_path, enc_file, key, iv, 'encrypt')
    t_enc = time.time() - start
    
    # Deszyfrowanie
    start = time.time()
    process_aes_cfb(enc_file, dec_file, key, iv, 'decrypt')
    t_dec = time.time() - start
    
    size_gb = os.path.getsize(file_path) / (1024**3)
    print(f"Szyfrowanie: {t_enc:.2f} s ({ (size_gb*1024)/t_enc:.2f} MB/s )")
    print(f"Deszyfrowanie: {t_dec:.2f} s")
  

if __name__ == "__main__":
    target_file = "test.mp4" 
    
    if os.path.exists(target_file):
        for size in [128, 192, 256]:
            run_experiment(target_file, size)
    else:
        print("Błąd: Brak pliku 10 GB!")
