a = int(input("Masukkan nilai a: "))
b = int(input("Masukkan nilai b: "))
c = a + b
print("Hasil dari Nilai C adalah :", c)

a = 10
b = 4
c = a + b
print("Hasil dari nilai c adalah", c)

A = 10
B = 10
if A == B:
    print("A dan B sama")

A = 10
B = 20
if A != B:
    print("A dan B tidak sama")

A = False
if not A:
    print("A adalah False, tapi not A menjadi True")

A = 5
A *= 2
print("A *= 2 →", A)

A = 10
A -= 3
print("A -= 3 →", A)

A = 10
A /= 2
print("A /= 2 →", A)

A = 10
A %= 2
print("A %= 2 →", A)

while input("Apakah Anda ingin memulai operasi perhitungan? (y/n): ").lower() == 'y':
    a = int(input("Masukkan nilai a: "))
    b = int(input("Masukkan nilai b: "))
    c = a + b
    print("Hasil dari Nilai C adalah:", c)
print("Program selesai. Terima kasih!")

import operator
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '^': operator.pow,
    '**': operator.pow,
}
a = float(input("Masukkan nilai a: "))
b = float(input("Masukkan nilai b: "))
c = input("Masukkan operator (+, -, *, /, %, ^, **): ")
c = input("Masukkan operator (+, -, *, /,%): ")

try:
    hasil = ops[c](a, b)
    print(f"Hasil dari {a} {c} {b} = {hasil}")
except KeyError:
    print("Operator tidak valid.")
except ZeroDivisionError:
    print("Pembagian dengan nol tidak diperbolehkan.")
