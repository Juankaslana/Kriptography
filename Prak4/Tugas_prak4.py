
import tkinter as tk
from tkinter import messagebox


def build_substitution_dict(mapping_text):
    """
    Membuat dictionary aturan substitusi dari input teks.
    Setiap baris berformat 'A B' atau 'A:B'.
    """
    mapping = {}
    for line in mapping_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            parts = line.split(':')
        else:
            parts = line.split()
        if len(parts) >= 2:
            k = parts[0].strip().upper()[0]
            v = parts[1].strip().upper()[0]
            mapping[k] = v
    return mapping



class FrameSubstitusi(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller
        tk.Label(self, text="Substitusi Cipher", font=("Arial", 12, "bold")).pack(anchor='w', pady=6)

      
        frame = tk.Frame(self)
        frame.pack(fill='x', pady=4)

        left = tk.Frame(frame)
        left.pack(side='left', padx=6)
        tk.Label(left, text="Aturan substitusi (baris: A B atau A:B):").pack(anchor='w')
        self.txt_rules = tk.Text(left, width=30, height=10)
        self.txt_rules.pack()
        self.txt_rules.insert(1.0, "U K\nN N\nI I\nK K\nA B")

        right = tk.Frame(frame)
        right.pack(side='left', fill='both', expand=True, padx=10)
        tk.Label(right, text="Plaintext:").pack(anchor='w')
        self.entry_plain = tk.Entry(right, width=50)
        self.entry_plain.pack(anchor='w', pady=4)
        tk.Button(right, text="Enkripsi Substitusi", command=self.run_substitusi).pack(anchor='w', pady=6)

    def run_substitusi(self):
        plaintext = self.entry_plain.get().upper()
        mapping = build_substitution_dict(self.txt_rules.get(1.0, tk.END))
        if not plaintext:
            messagebox.showerror("Error", "Masukkan plaintext terlebih dahulu.")
            return

        ciphertext = ""
        for ch in plaintext:
            if ch in mapping:
                ciphertext += mapping[ch]
            else:
                ciphertext += ch

        output = f"Plaintext: {plaintext}\nCiphertext: {ciphertext}\nAturan: {mapping}"
        self.ctrl.write_output(output, clear=True)



class FrameTransposisi(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller
        tk.Label(self, text="Transposisi Cipher", font=("Arial", 12, "bold")).pack(anchor='w', pady=6)

        tk.Label(self, text="Masukkan plaintext:").pack(anchor='w')
        self.entry_plain = tk.Entry(self, width=70)
        self.entry_plain.pack(anchor='w', pady=4)

        tk.Label(self, text="(Opsional) panjang blok per bagian (kosong = otomatis):").pack(anchor='w')
        self.entry_block = tk.Entry(self, width=10)
        self.entry_block.pack(anchor='w', pady=4)

        tk.Button(self, text="Enkripsi Transposisi", command=self.run_transposisi).pack(anchor='w', pady=6)
        tk.Button(self, text="Tampilkan Proses", command=self.run_verbose).pack(anchor='w', pady=4)

    def transposisi(self, plaintext, part_len=None, verbose=False):
        if not plaintext:
            return "", [], []

        if part_len is None or part_len <= 0:
            part_len = max(1, len(plaintext) // 4)

        parts = [plaintext[i:i + part_len] for i in range(0, len(plaintext), part_len)]
        ciphertext = ""
        logs = []

        for col in range(4):
            for idx, part in enumerate(parts):
                if col < len(part):
                    ch = part[col]
                    ciphertext += ch
                    if verbose:
                        logs.append(f"Menambahkan '{ch}' dari Bagian {idx+1} ke ciphertext.")

        return ciphertext, parts, logs

    def run_transposisi(self):
        plain = self.entry_plain.get()
        try:
            block = int(self.entry_block.get()) if self.entry_block.get() else None
        except:
            messagebox.showerror("Error", "Panjang blok harus berupa angka.")
            return

        cipher, _, _ = self.transposisi(plain, block, verbose=False)
        out = f"Plaintext: {plain}\nCiphertext: {cipher}"
        self.ctrl.write_output(out, clear=True)

    def run_verbose(self):
        plain = self.entry_plain.get()
        try:
            block = int(self.entry_block.get()) if self.entry_block.get() else None
        except:
            messagebox.showerror("Error", "Panjang blok harus berupa angka.")
            return

        cipher, parts, logs = self.transposisi(plain, block, verbose=True)
        out = f"Plaintext: {plain}\n\nBagian plaintext:"
        for i, p in enumerate(parts):
            out += f"\nBagian {i+1}: '{p}'"
        out += "\n\nProses pembentukan:"
        for l in logs:
            out += "\n" + l
        out += f"\n\nCiphertext: {cipher}"
        self.ctrl.write_output(out, clear=True)



class FrameGabungan(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller
        tk.Label(self, text="Gabungan Substitusi + Transposisi", font=("Arial", 12, "bold")).pack(anchor='w', pady=6)

        frame = tk.Frame(self)
        frame.pack(fill='x', pady=4)

        left = tk.Frame(frame)
        left.pack(side='left', padx=6)
        tk.Label(left, text="Aturan substitusi (baris: A B atau A:B):").pack(anchor='w')
        self.txt_rules = tk.Text(left, width=28, height=10)
        self.txt_rules.pack()
        self.txt_rules.insert(1.0, "U K\nN N\nI I\nK K\nA B")

        right = tk.Frame(frame)
        right.pack(side='left', padx=10)
        tk.Label(right, text="Plaintext:").pack(anchor='w')
        self.entry_plain = tk.Entry(right, width=60)
        self.entry_plain.pack(anchor='w', pady=4)

        tk.Label(right, text="(Opsional) Panjang blok transposisi:").pack(anchor='w')
        self.entry_block = tk.Entry(right, width=10)
        self.entry_block.pack(anchor='w', pady=4)

        tk.Button(right, text="Enkripsi Gabungan", command=self.run_combo).pack(anchor='w', pady=6)
        tk.Button(right, text="Enkripsi Gabungan + Proses", command=self.run_combo_verbose).pack(anchor='w', pady=4)

    def substitusi(self, plaintext, mapping):
        result = ""
        for ch in plaintext.upper():
            if ch in mapping:
                result += mapping[ch]
            else:
                result += ch
        return result

    def transposisi(self, plaintext, part_len=None):
        if part_len is None or part_len <= 0:
            part_len = max(1, len(plaintext) // 4)
        parts = [plaintext[i:i + part_len] for i in range(0, len(plaintext), part_len)]
        ciphertext = ""
        for col in range(4):
            for part in parts:
                if col < len(part):
                    ciphertext += part[col]
        return ciphertext, parts

    def run_combo(self):
        plain = self.entry_plain.get().upper()
        rules = build_substitution_dict(self.txt_rules.get(1.0, tk.END))
        if not plain:
            messagebox.showerror("Error", "Masukkan plaintext.")
            return

        sub = self.substitusi(plain, rules)
        try:
            block = int(self.entry_block.get()) if self.entry_block.get() else None
        except:
            messagebox.showerror("Error", "Panjang blok harus berupa angka.")
            return

        trans, _ = self.transposisi(sub, block)
        out = (f"Input Plaintext: {plain}\n"
               f"Cipher (Substitusi): {sub}\n"
               f"Cipher (Setelah Transposisi): {trans}")
        self.ctrl.write_output(out, clear=True)

    def run_combo_verbose(self):
        plain = self.entry_plain.get().upper()
        rules = build_substitution_dict(self.txt_rules.get(1.0, tk.END))
        if not plain:
            messagebox.showerror("Error", "Masukkan plaintext.")
            return

        sub = self.substitusi(plain, rules)
        try:
            block = int(self.entry_block.get()) if self.entry_block.get() else None
        except:
            messagebox.showerror("Error", "Panjang blok harus berupa angka.")
            return

        trans, parts = self.transposisi(sub, block)
        out = f"Plaintext: {plain}\n\nSetelah Substitusi:\n{sub}\n\nBagian untuk Transposisi:"
        for i, p in enumerate(parts):
            out += f"\nBagian {i+1}: '{p}'"
        out += f"\n\nCipher Akhir: {trans}"
        self.ctrl.write_output(out, clear=True)



class Praktikum4App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tugas Praktikum 4 - Kriptografi Klasik")
        self.geometry("760x560")
        self.resizable(False, False)

        
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill='x', padx=8, pady=6)
        tk.Label(menu_frame, text="Pilih Fitur:", font=("Arial", 11, "bold")).pack(side='left')
        tk.Button(menu_frame, text="Substitusi Cipher", command=self.show_sub).pack(side='left', padx=6)
        tk.Button(menu_frame, text="Transposisi Cipher", command=self.show_trans).pack(side='left', padx=6)
        tk.Button(menu_frame, text="Gabungan Cipher", command=self.show_combo).pack(side='left', padx=6)

        
        self.container = tk.Frame(self)
        self.container.pack(fill='both', expand=True, padx=8, pady=(0, 8))

       
        output_frame = tk.Frame(self)
        output_frame.pack(fill='both', expand=False, padx=8, pady=(0, 8))
        tk.Label(output_frame, text="Output:", anchor='w').pack(fill='x')
        self.text_out = tk.Text(output_frame, height=14, wrap='word')
        self.text_out.pack(fill='both', expand=True)

        
        self.frames = {}
        for F in (FrameSubstitusi, FrameTransposisi, FrameGabungan):
            page = F(self.container, self)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky='nsew')

        self.show_sub()


    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        self.clear_output()

    def show_sub(self):
        self.show_frame("FrameSubstitusi")

    def show_trans(self):
        self.show_frame("FrameTransposisi")

    def show_combo(self):
        self.show_frame("FrameGabungan")

    # Output handler
    def write_output(self, text, clear=False):
        if clear:
            self.text_out.delete(1.0, tk.END)
        self.text_out.insert(tk.END, text + "\n")
        self.text_out.see(tk.END)

    def clear_output(self):
        self.text_out.delete(1.0, tk.END)



if __name__ == "__main__":
    app = Praktikum4App()
    app.mainloop()
