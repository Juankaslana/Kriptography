import tkinter as tk
from tkinter import messagebox

# ------------------- PROGRAM 1: Kalkulator interaktif -------------------
def kalkulator_interaktif(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Kalkulator Interaktif", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(frame, text="Angka 1:").pack()
    angka1 = tk.Entry(frame)
    angka1.pack()

    tk.Label(frame, text="Angka 2:").pack()
    angka2 = tk.Entry(frame)
    angka2.pack()

    tk.Label(frame, text="Operator (+ - * /):").pack()
    operator = tk.Entry(frame)
    operator.pack()

    def hitung():
        try:
            a = float(angka1.get())
            b = float(angka2.get())
            op = operator.get()
            if op == '+':
                hasil = a + b
            elif op == '-':
                hasil = a - b
            elif op == '*':
                hasil = a * b
            elif op == '/':
                if b == 0:
                    messagebox.showerror("Error", "Pembagian dengan nol tidak diizinkan")
                    return
                hasil = a / b
            else:
                messagebox.showerror("Error", "Operator tidak valid")
                return
            messagebox.showinfo("Hasil", f"Hasil: {hasil}")
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka valid")

    tk.Button(frame, text="Hitung", command=hitung, bg="lightblue").pack(pady=10)
    tk.Button(frame, text="Kembali", command=lambda: menu_utama(frame), bg="lightgrey").pack()

# ------------------- PROGRAM 2: Kalkulator fungsi -------------------
def kalkulator_fungsi(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Kalkulator Fungsi", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(frame, text="Angka 1:").pack()
    angka1 = tk.Entry(frame)
    angka1.pack()

    tk.Label(frame, text="Angka 2:").pack()
    angka2 = tk.Entry(frame)
    angka2.pack()

    def hitung():
        try:
            a = float(angka1.get())
            b = float(angka2.get())
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka valid")
            return
        hasil = (
            f"Penjumlahan: {a+b}\n"
            f"Pengurangan: {a-b}\n"
            f"Perkalian  : {a*b}\n"
            f"Pembagian  : {'Error (bagi 0)' if b==0 else a/b}"
        )
        messagebox.showinfo("Hasil", hasil)

    tk.Button(frame, text="Hitung Semua", command=hitung, bg="lightgreen").pack(pady=10)
    tk.Button(frame, text="Kembali", command=lambda: menu_utama(frame), bg="lightgrey").pack()

# ------------------- PROGRAM 3: Hitung Nilai Akademik -------------------
def hitung_nilai_akhir(sikap, tugas, uts, uas):
    return (sikap * 0.10) + (tugas * 0.30) + (uts * 0.25) + (uas * 0.35)

def konversi_nilai(nilai):
    if 81 <= nilai <= 100: return "A", 4
    elif 76 <= nilai <= 80: return "B+", 3.5
    elif 71 <= nilai <= 75: return "B", 3
    elif 66 <= nilai <= 70: return "C+", 2.5
    elif 56 <= nilai <= 65: return "C", 2
    elif 46 <= nilai <= 55: return "D", 1
    else: return "E", 0

def keterangan(nilai):
    return "Lulus" if nilai >= 56 else "Tidak Lulus"

def akademik(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Hitung Nilai Akademik", font=("Arial", 14, "bold")).pack(pady=10)

    entries = {}
    for label in ["Sikap/Kehadiran (10%)", "Tugas (30%)", "UTS (25%)", "UAS (35%)"]:
        tk.Label(frame, text=label).pack()
        e = tk.Entry(frame)
        e.pack()
        entries[label] = e

    def hitung():
        try:
            sikap = float(entries["Sikap/Kehadiran (10%)"].get())
            tugas = float(entries["Tugas (30%)"].get())
            uts = float(entries["UTS (25%)"].get())
            uas = float(entries["UAS (35%)"].get())
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka valid")
            return

        total = hitung_nilai_akhir(sikap, tugas, uts, uas)
        huruf, bobot = konversi_nilai(total)
        status = keterangan(total)

        hasil = (
            f"Total Nilai Akhir: {total:.2f}\n"
            f"Nilai Huruf      : {huruf}\n"
            f"Bobot Nilai      : {bobot}\n"
            f"Keterangan       : {status}"
        )
        messagebox.showinfo("Hasil Akademik", hasil)

    tk.Button(frame, text="Hitung Nilai", command=hitung, bg="orange").pack(pady=10)
    tk.Button(frame, text="Kembali", command=lambda: menu_utama(frame), bg="lightgrey").pack()

# ------------------- MENU UTAMA -------------------
def menu_utama(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Menu Utama", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(frame, text="Kalkulator Interaktif", command=lambda: kalkulator_interaktif(frame), width=25, bg="lightblue").pack(pady=5)
    tk.Button(frame, text="Kalkulator Fungsi", command=lambda: kalkulator_fungsi(frame), width=25, bg="lightgreen").pack(pady=5)
    tk.Button(frame, text="Hitung Nilai Akademik", command=lambda: akademik(frame), width=25, bg="orange").pack(pady=5)
    tk.Button(frame, text="Keluar", command=root.destroy, width=25, bg="red", fg="white").pack(pady=10)

# ------------------- MAIN -------------------
root = tk.Tk()
root.title("Program Multi Fungsi")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

menu_utama(frame)

root.mainloop()
