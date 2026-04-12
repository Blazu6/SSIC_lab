#!/bin/bash

rm -rf run_*.bit
rm -f templates/templates

files=("same_zera_sha3_256.bit" "same_zera_sha3_512.bit" "TRNG_P_sha3_256.bit" "TRNG_P_sha3_512.bit")
bitestream=100
LENGTH=1000000

echo "Mam do sprawdzenia: ${#files[@]} pliki."

for file in "${files[@]}"; do
    WORK_DIR="run_$file"
    mkdir -p "$WORK_DIR"

    cp -r templates "$WORK_DIR/"
    cp assess "$WORK_DIR/"
    cp "$file" "$WORK_DIR/data.bit"
    
    cp -r experiments "$WORK_DIR/"
    
    find "$WORK_DIR/experiments" -name "*.txt" -delete

    echo "Uruchamiam analizę: $file..."

    (
        cd "$WORK_DIR" || exit
        # Podajemy parametry: 0 (plik), data.bit, 1 (wszystkie), 0 (dalej), $bitestream, 1 (binarny)
        printf "0\ndata.bit\n1\n0\n$bitestream\n1\n" | ./assess $LENGTH > debug_output.log 2>&1
        echo "Zakończono: $file"
    ) &
done

wait
echo "--- WSZYSTKIE TESTY ZAKOŃCZONE ---"