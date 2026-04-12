from Crypto.Hash import SHA3_256, SHA3_512
import os

def sha3_256(input_path: str, output_path: str) -> int:
    count = 0

    try:
        with open(input_path, 'rb') as f, \
            open(output_path, 'wb') as out_file:

            while chunk := f.read(128):
                h = SHA3_256.new()
                h.update(chunk)
                block_hash = h.digest()
                out_file.write(block_hash)
                count += 1
        
        return count

    except FileNotFoundError:
        print(f"Plik {input_path} nie został znaleziony.")
        return None
    except IOError as e:
        print(f"Wystąpił błąd podczas odczytu lub zapisu pliku: {e}")
        return None

def sha3_512(input_path: str, output_path: str) -> int:
    count = 0

    try:
        with open(input_path, 'rb') as f, \
            open(output_path, 'wb') as out_file:

            while chunk := f.read(256):
                h = SHA3_512.new()
                h.update(chunk)
                block_hash = h.digest()
                out_file.write(block_hash)
                count += 1    
        return count

    except FileNotFoundError:
        print(f"Plik {input_path} nie został znaleziony.")
        return None
    except IOError as e:
        print(f"Wystąpił błąd podczas odczytu lub zapisu pliku: {e}")
        return None
        



if __name__ == "__main__":
    #pliki wejsciowe
    input_file1 = 'same_zera.bit'
    input_file2 = 'TRNG_P.bit'
    #pliki wyjsciowe 256
    output_file_256_1 = 'same_zera_sha3_256.bit'
    output_file_256_2 = 'TRNG_P_sha3_256.bit'
    #pliki wyjsciowe 512
    output_file_512_1 = 'same_zera_sha3_512.bit'
    output_file_512_2 = 'TRNG_P_sha3_512_2.bit'
    
    print(f"--- Rozpoczynam pracę na pliku: {input_file1} ---")
    res1 = sha3_256(input_file1, output_file_256_1)
    res1_512 = sha3_512(input_file1, output_file_512_1)
    print(f"Rozpoczynam praceę na pliku: {input_file2} ---")
    res2 = sha3_256(input_file2, output_file_256_2)
    res2_512 = sha3_512(input_file2, output_file_512_2)