# =============================================
# Program Konversi Bilangan (Biner, Oktal, Hexa)
# Dibuat oleh: Juan Sirait
# =============================================

def biner_ke_desimal_hexa():
    biner = input("Masukkan bilangan biner: ")
    try:
        desimal = int(biner, 2)
        hexa = hex(desimal).upper().replace("0X", "")
        print(f"Desimal     : {desimal}")
        print(f"Hexadesimal : {hexa}")
    except ValueError:
        print("Input tidak valid! Pastikan hanya berisi 0 dan 1.")

def oktal_ke_desimal_biner_hexa():
    oktal = input("Masukkan bilangan oktal: ")
    try:
        desimal = int(oktal, 8)
        biner = bin(desimal).replace("0b", "")
        hexa = hex(desimal).upper().replace("0X", "")
        print(f"Desimal     : {desimal}")
        print(f"Biner       : {biner}")
        print(f"Hexadesimal : {hexa}")
    except ValueError:
        print("Input tidak valid! Pastikan hanya berisi angka 0–7.")

def hexa_ke_desimal_biner_oktal():
    hexa = input("Masukkan bilangan hexadesimal: ")
    try:
        desimal = int(hexa, 16)
        biner = bin(desimal).replace("0b", "")
        oktal = oct(desimal).replace("0o", "")
        print(f"Desimal : {desimal}")
        print(f"Biner   : {biner}")
        print(f"Oktal   : {oktal}")
    except ValueError:
        print("Input tidak valid! Pastikan hanya menggunakan 0–9 dan A–F.")

def menu():
    while True:
        print("\n=== PROGRAM KONVERSI BILANGAN ===")
        print("1. Konversi Biner → Desimal & Hexadesimal")
        print("2. Konversi Oktal → Desimal, Biner & Hexadesimal")
        print("3. Konversi Hexadesimal → Desimal, Biner & Oktal")
        print("4. Keluar")
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            biner_ke_desimal_hexa()
        elif pilihan == "2":
            oktal_ke_desimal_biner_hexa()
        elif pilihan == "3":
            hexa_ke_desimal_biner_oktal()
        elif pilihan == "4":
            print("ADIOS!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Jalankan program
if __name__ == "__main__":
    menu()
