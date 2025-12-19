import tkinter as tk
from tkinter import messagebox
from math import gcd

# =============================
# UTIL
# =============================
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def modinv(a, p):
    return pow(a, p - 2, p)

# =============================
# ELGAMAL CORE
# =============================
def encrypt_number(m, p, g, y, k):
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p)) % p
    return c1, c2

def decrypt_number(c1, c2, p, x):
    s = pow(c1, x, p)
    return (c2 * modinv(s, p)) % p

# =============================
# GUI LOGIC
# =============================
def encrypt():
    try:
        p = int(entry_p.get())
        g = int(entry_g.get())
        x = int(entry_x.get())
        k = int(entry_k.get())
        text = entry_plain.get()

        # VALIDASI ELGAMAL
        if not is_prime(p):
            raise ValueError("p harus bilangan prima")
        if not (1 < g < p):
            raise ValueError("g harus lebih kecil dari p")
        if not (1 < x < p - 1):
            raise ValueError("x harus 1 < x < p-1")
        if not (1 < k < p - 1):
            raise ValueError("k harus 1 < k < p-1")
        if gcd(k, p - 1) != 1:
            raise ValueError("k harus relatif prima terhadap (p-1)")

        y = pow(g, x, p)

        encrypted = []

        if text.isdigit():
            m = int(text)
            if m >= p:
                raise ValueError("Pesan harus < p")
            c1, c2 = encrypt_number(m, p, g, y, k)
            encrypted.append(f"{c1},{c2}")
        else:
            for ch in text:
                m = ord(ch)
                if m >= p:
                    raise ValueError("Kode ASCII karakter >= p")
                c1, c2 = encrypt_number(m, p, g, y, k)
                encrypted.append(f"{c1},{c2}")

        entry_cipher.delete(0, tk.END)
        entry_cipher.insert(0, " | ".join(encrypted))

    except ValueError as e:
        messagebox.showerror("Validasi ElGamal Gagal", str(e))
    except:
        messagebox.showerror("Error", "Input tidak valid")

def decrypt():
    try:
        p = int(entry_p.get())
        x = int(entry_x.get())
        blocks = entry_cipher.get().split(" | ")

        nums = []
        text = ""

        for b in blocks:
            c1, c2 = map(int, b.split(","))
            m = decrypt_number(c1, c2, p, x)
            nums.append(str(m))
            if 32 <= m <= 126:
                text += chr(m)

        entry_dec_num.delete(0, tk.END)
        entry_dec_text.delete(0, tk.END)

        entry_dec_num.insert(0, " ".join(nums))
        entry_dec_text.insert(0, text)

    except:
        messagebox.showerror("Error", "Dekripsi gagal")

# =============================
# GUI
# =============================
root = tk.Tk()
root.title("ElGamal GUI (Manual & Validasi)")
root.geometry("600x480")

tk.Label(root, text="ELGAMAL ENKRIPSI & DEKRIPSI", font=("Arial", 14, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="p (prima)").grid(row=0, column=0, sticky="w")
entry_p = tk.Entry(frame)
entry_p.grid(row=0, column=1)

tk.Label(frame, text="g (generator)").grid(row=1, column=0, sticky="w")
entry_g = tk.Entry(frame)
entry_g.grid(row=1, column=1)

tk.Label(frame, text="x (private key)").grid(row=2, column=0, sticky="w")
entry_x = tk.Entry(frame)
entry_x.grid(row=2, column=1)

tk.Label(frame, text="k (random)").grid(row=3, column=0, sticky="w")
entry_k = tk.Entry(frame)
entry_k.grid(row=3, column=1)

tk.Label(frame, text="Plaintext (Angka / Teks)").grid(row=4, column=0, sticky="w")
entry_plain = tk.Entry(frame, width=40)
entry_plain.grid(row=4, column=1)

tk.Button(root, text="Enkripsi", command=encrypt).pack(pady=8)

tk.Label(frame, text="Ciphertext").grid(row=5, column=0, sticky="w")
entry_cipher = tk.Entry(frame, width=40)
entry_cipher.grid(row=5, column=1)

tk.Button(root, text="Dekripsi", command=decrypt).pack(pady=8)

tk.Label(frame, text="Hasil Angka").grid(row=6, column=0, sticky="w")
entry_dec_num = tk.Entry(frame, width=40)
entry_dec_num.grid(row=6, column=1)

tk.Label(frame, text="Hasil Teks").grid(row=7, column=0, sticky="w")
entry_dec_text = tk.Entry(frame, width=40)
entry_dec_text.grid(row=7, column=1)

root.mainloop()
