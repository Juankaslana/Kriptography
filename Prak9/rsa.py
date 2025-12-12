import tkinter as tk
from tkinter import messagebox
import random

# -----------------------
#       UTILITAS
# -----------------------

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def gen_prime(min_val=50, max_val=200):
    while True:
        x = random.randint(min_val, max_val)
        if is_prime(x):
            return x

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# -----------------------
#   LATIHAN 1 (p,q,e tetap)
# -----------------------

def generate_L1():
    global p, q, e, n, phi, d

    p = 17
    q = 11
    e = 7
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)

    txt_info.delete('1.0', tk.END)
    txt_info.insert(tk.END, "[Latihan 1 - p,q,e Tetap]\n")
    txt_info.insert(tk.END, f"p = {p}\nq = {q}\ne = {e}\n")
    txt_info.insert(tk.END, f"n = {n}\nphi = {phi}\nd = {d}\n")

# -----------------------
#   LATIHAN 2 (acak)
# -----------------------

def generate_L2():
    global p, q, e, n, phi, d

    p = gen_prime()
    q = gen_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(3, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    d = modinv(e, phi)

    txt_info.delete('1.0', tk.END)
    txt_info.insert(tk.END, "[Latihan 2 - p,q,e Acak]\n")
    txt_info.insert(tk.END, f"p = {p}\nq = {q}\ne = {e}\n")
    txt_info.insert(tk.END, f"n = {n}\nphi = {phi}\nd = {d}\n")

# -----------------------
#   ENKRIPSI / DEKRIPSI
# -----------------------

def encrypt():
    plaintext = entry_plain.get().strip()
    if not plaintext:
        messagebox.showerror("Error", "Plaintext kosong.")
        return
    
    if n == 0:
        messagebox.showerror("Error", "Silakan pilih Latihan 1 atau 2 dahulu.")
        return

    ciphertext_list = []
    debug_output = []

    for ch in plaintext:
        m = ord(ch)

        if m >= n:
            messagebox.showerror("Error", f"ASCII {m} (char '{ch}') >= n ({n})")
            return
        
        c = pow(m, e, n)
        ciphertext_list.append(str(c))

        debug_output.append(
            f"'{ch}' → ASCII {m} → {m}^{e} mod {n} = {c}"
        )

    entry_cipher.delete(0, tk.END)
    entry_cipher.insert(0, " ".join(ciphertext_list))

    txt_output.delete('1.0', tk.END)
    txt_output.insert(tk.END, "[DEBUG ENKRIPSI]\n")
    for line in debug_output:
        txt_output.insert(tk.END, line + "\n")


def decrypt():
    cipher_text = entry_cipher.get().strip().split()

    if not cipher_text:
        messagebox.showerror("Error", "Ciphertext kosong.")
        return

    try:
        cipher_ints = [int(x) for x in cipher_text]
    except:
        messagebox.showerror("Error", "Ciphertext harus berupa angka.")
        return

    plaintext = ""
    debug_output = []

    for c in cipher_ints:
        m = pow(c, d, n)
        plaintext += chr(m)

        debug_output.append(
            f"{c}^{d} mod {n} = {m} → '{chr(m)}'"
        )

    txt_output.delete('1.0', tk.END)
    txt_output.insert(tk.END, "[DEBUG DEKRIPSI]\n")
    for line in debug_output:
        txt_output.insert(tk.END, line + "\n")

# -----------------------
#   GUI
# -----------------------

root = tk.Tk()
root.title("RSA GUI – Praktikum (Latihan 1 & 2)")
root.geometry("650x650")

# Tombol L1 dan L2
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

btn_l1 = tk.Button(frame_top, text="Latihan 1: p=17,q=11,e=7", width=25, command=generate_L1)
btn_l1.grid(row=0, column=0, padx=5)

btn_l2 = tk.Button(frame_top, text="Latihan 2: p,q,e Acak (50–200)", width=25, command=generate_L2)
btn_l2.grid(row=0, column=1, padx=5)

# Area info kunci
txt_info = tk.Text(root, height=7, width=70)
txt_info.pack()

# Input plaintext
tk.Label(root, text="Plaintext:").pack()
entry_plain = tk.Entry(root, width=50)
entry_plain.pack()

tk.Button(root, text="Encrypt", command=encrypt).pack(pady=3)

# Ciphertext
tk.Label(root, text="Ciphertext (angka):").pack()
entry_cipher = tk.Entry(root, width=50)
entry_cipher.pack()

tk.Button(root, text="Decrypt", command=decrypt).pack(pady=3)

# Output debug
txt_output = tk.Text(root, height=18, width=80)
txt_output.pack()

# Variabel RSA global
p = q = e = n = phi = d = 0

root.mainloop()
