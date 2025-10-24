import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess, sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def tambah(a, b): return a + b 
def kurang(a, b): return a - b 
def kali(a, b): return a * b 
def bagi(a, b): 
    if b != 0: 
        return a / b 
    else: 
        return "Error: Pembagian dengan nol"

def kalkulator_popup():
    try:
        angka1 = float(simpledialog.askstring("Input", "Masukkan angka pertama:"))
        angka2 = float(simpledialog.askstring("Input", "Masukkan angka kedua:"))
        operator = simpledialog.askstring("Input", "Masukkan operator (+, -, *, /):")
    except:
        messagebox.showerror("Error", "Input tidak valid!")
        return

    if operator == '+':
        hasil = tambah(angka1, angka2)
    elif operator == '-':
        hasil = kurang(angka1, angka2)
    elif operator == '*':
        hasil = kali(angka1, angka2)
    elif operator == '/':
        hasil = bagi(angka1, angka2)
    else:
        messagebox.showerror("Error", "Operator tidak valid!")
        return

    messagebox.showinfo("Hasil Kalkulator", f"Hasil: {hasil}")

def kembali():
    root.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "main.py")])

root = tk.Tk()
root.title("Kalkulator Operator - test2.py")
root.geometry("300x200")

tk.Label(root, text="📌 Kalkulator dengan Operator", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(root, text="Mulai Kalkulator", command=kalkulator_popup, width=20, bg="lightgreen").pack(pady=5)
tk.Button(root, text="⬅ Kembali ke Menu Utama", command=kembali, width=25, bg="orange").pack(pady=15)

root.mainloop()
