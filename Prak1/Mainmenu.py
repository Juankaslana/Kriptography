import tkinter as tk
import subprocess
import sys
import os

# Ambil path folder saat ini (kriptograpi)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    """Jalankan file python lain dalam folder kriptograpi"""
    script_path = os.path.join(BASE_DIR, script_name)
    try:
        subprocess.Popen([sys.executable, script_path])  # buka program baru
    except Exception as e:
        print(f"Gagal menjalankan {script_name}: {e}")

def menu_utama(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="📌 MENU UTAMA", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(frame, text="➡ Jalankan test.py", 
              command=lambda: run_script("test.py"), 
              width=25, bg="lightblue").pack(pady=5)

    tk.Button(frame, text="➡ Jalankan test2.py", 
              command=lambda: run_script("test2.py"), 
              width=25, bg="lightgreen").pack(pady=5)

    tk.Button(frame, text="➡ Jalankan import.py", 
              command=lambda: run_script("import.py"), 
              width=25, bg="orange").pack(pady=5)

    tk.Button(frame, text="❌ Keluar", 
              command=root.destroy, 
              width=25, bg="red", fg="white").pack(pady=15)

# ------------------- MAIN PROGRAM -------------------
root = tk.Tk()
root.title("Program Multi File - Kriptograpi")
root.geometry("350x280")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

menu_utama(frame)

root.mainloop()
