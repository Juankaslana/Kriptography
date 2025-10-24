temperature = 30
if temperature > 25:
    print("Cuaca panas, nyalakan AC")

password = "12345"
if password == "secret":
    print("Akses diterima")
else:
    print("Akses ditolak")

nilai = 85
if nilai >= 90:
    print("Anda mendapat nilai A")
elif nilai >= 80:
    print("Anda mendapat nilai B")
elif nilai >= 70:
    print("Anda mendapat nilai C")
else:
    print("Perbaiki nilai")

number = 10
if number > 0:
    print("Angka positif")
    if number % 2 == 0:
        print("Angka genap")
    else:
        print("Angka ganjil")
else:
    print("Angka negatif")

umur = 20
tinggi = 160
if umur >= 18 and tinggi >= 155:
    print("Anda memenuhi syarat")
else:
    print("Anda tidak memenuhi syarat")

day = "Sunday"
if day == "Saturday" or day == "Sunday":
    print("Ini adalah akhir pekan.")
else:
    print("Ini adalah hari kerja.")

is_logged_in = False
if not is_logged_in:
    print("Silakan masuk untuk melanjutkan.")
else:
    print("Selamat datang kembali!")

username = input("Masukkan nama pengguna: ")
if username == "admin":
    print("Selamat datang, admin!")
else:
    print(f"Selamat datang, {username}!")

a = float(input("Masukkan nilai a: "))
b = float(input("Masukkan nilai b: "))
op = input("Masukkan operator (+, -, *, /): ")

if op == '+':
    print(f"Hasil dari {a} + {b} =", a + b)
elif op == '-':
    print(f"Hasil dari {a} - {b} =", a - b)
elif op == '*':
    print(f"Hasil dari {a} * {b} =", a * b)
elif op == '/':
    if b != 0:
        print(f"Hasil dari {a} / {b} =", a / b)
    else:
        print("Pembagian dengan nol tidak diperbolehkan.")
else:
    print("Operator tidak dikenali.")


