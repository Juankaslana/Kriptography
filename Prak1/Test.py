import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess, sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def tambah(a, b): 
    return a + b 
def kurang(a, b): 
    return a - b 
def kali(a, b): 
    return a * b 
def bagi(a, b): 
    if b != 0: 
        return a / b 
    else: 
        return "Error: Pembagian dengan nol"

def operasi_langsung():
    try:
        angka1 = float(simpledialog.askstring("Input", "Masukkan angka pertama:"))
        angka2 = float(simpledialog.askstring("Input", "Masukkan angka kedua:"))
    except:
        messagebox.showerror("Error", "Input tidak valid!")
        return

    hasil = (
        f"Hasil penjumlahan : {tambah(angka1, angka2)}\n"
        f"Hasil pengurangan : {kurang(angka1, angka2)}\n"
        f"Hasil perkalian   : {kali(angka1, angka2)}\n"
        f"Hasil pembagian   : {bagi(angka1, angka2)}"
    )
    messagebox.showinfo("Hasil Operasi", hasil)

def kembali():
    root.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "main.py")])

root = tk.Tk()
root.title("Operasi Langsung - test.py")
root.geometry("300x200")

tk.Label(root, text="📌 Operasi Langsung (Semua Hasil)", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(root, text="Mulai Hitung", command=operasi_langsung, width=20, bg="lightblue").pack(pady=5)
tk.Button(root, text="⬅ Kembali ke Menu Utama", command=kembali, width=25, bg="orange").pack(pady=15)

root.mainloop()
