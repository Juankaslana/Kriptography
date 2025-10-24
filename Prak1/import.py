import tkinter as tk

def hitung_nilai_akhir(sikap, tugas, uts, uas):
    return (sikap * 0.10) + (tugas * 0.30) + (uts * 0.25) + (uas * 0.35)

def konversi_nilai(nilai):
    if 81 <= nilai <= 100:
        return "A", 4
    elif 76 <= nilai <= 80:
        return "B+", 3.5
    elif 71 <= nilai <= 75:
        return "B", 3
    elif 66 <= nilai <= 70:
        return "C+", 2.5
    elif 56 <= nilai <= 65:
        return "C", 2
    elif 46 <= nilai <= 55:
        return "D", 1
    else:
        return "E", 0

def keterangan(nilai):
    return "Lulus" if nilai >= 56 else "Tidak Lulus"

def proses_hitung():
    try:
        sikap = float(entry_sikap.get())
        tugas = float(entry_tugas.get())
        uts = float(entry_uts.get())
        uas = float(entry_uas.get())
    except ValueError:
        label_hasil.config(text="⚠️ Input tidak valid, masukkan angka!", fg="red")
        return

    total = hitung_nilai_akhir(sikap, tugas, uts, uas)
    huruf, bobot = konversi_nilai(total)
    status = keterangan(total)

    hasil_text = (
        f"Total Nilai Akhir : {total:.2f}\n"
        f"Nilai Huruf       : {huruf}\n"
        f"Bobot Nilai       : {bobot}\n"
        f"Keterangan        : {status}"
    )
    label_hasil.config(text=hasil_text, fg="black")

# --- GUI ---
root = tk.Tk()
root.title("Hitung Nilai Akademik")

tk.Label(root, text="Program Hitung Nilai Akhir Akademik", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(root, text="Sikap/Kehadiran (10%)").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_sikap = tk.Entry(root)
entry_sikap.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Tugas (30%)").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_tugas = tk.Entry(root)
entry_tugas.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="UTS (25%)").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_uts = tk.Entry(root)
entry_uts.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="UAS (35%)").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_uas = tk.Entry(root)
entry_uas.grid(row=4, column=1, padx=10, pady=5)

btn_hitung = tk.Button(root, text="Hitung Nilai", command=proses_hitung, bg="lightblue", font=("Arial", 11, "bold"))
btn_hitung.grid(row=5, column=0, columnspan=2, pady=15)

# Label hasil (kosong dulu, nanti diisi setelah hitung)
label_hasil = tk.Label(root, text="", font=("Arial", 11), justify="left")
label_hasil.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
