
import tkinter as tk
from tkinter import messagebox
from itertools import permutations, combinations
import math

class Praktikum3App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tugas Praktikum 3")
        self.geometry("700x520")
        self.resizable(False, False)

     
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill='x', padx=8, pady=6)

        tk.Label(menu_frame, text="Praktikum 3 - Pilih Fitur:", font=("Arial", 11, "bold")).pack(side='left')
        tk.Button(menu_frame, text="Konversi Bilangan", command=self.show_conv).pack(side='left', padx=6)
        tk.Button(menu_frame, text="Permutasi", command=self.show_perm).pack(side='left', padx=6)
        tk.Button(menu_frame, text="Kombinasi", command=self.show_comb).pack(side='left', padx=6)

       
        self.container = tk.Frame(self)
        self.container.pack(fill='both', expand=True, padx=8, pady=(0, 8))

    
        output_frame = tk.Frame(self)
        output_frame.pack(fill='both', expand=False, padx=8, pady=(0, 8))
        tk.Label(output_frame, text="Output:", anchor='w').pack(fill='x')
        self.text_out = tk.Text(output_frame, height=12, wrap='word')
        self.text_out.pack(fill='both', expand=True)

       
        self.frames = {}
        for F in (FrameKonversi, FramePermutasi, FrameKombinasi):
            page = F(self.container, self)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky='nsew')

        self.show_conv()

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        self.clear_output()

    def show_conv(self):
        self.show_frame("FrameKonversi")

    def show_perm(self):
        self.show_frame("FramePermutasi")

    def show_comb(self):
        self.show_frame("FrameKombinasi")

    def write_output(self, text, clear=False):
        if clear:
            self.text_out.delete(1.0, tk.END)
        self.text_out.insert(tk.END, text + "\n")
        self.text_out.see(tk.END)

    def clear_output(self):
        self.text_out.delete(1.0, tk.END)



class FrameKonversi(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller

        tk.Label(self, text="Konversi Bilangan", font=("Arial", 12, "bold")).pack(anchor='w', pady=6)
        frm = tk.Frame(self)
        frm.pack(anchor='w', pady=4)

        tk.Label(frm, text="Masukkan nilai: ").grid(row=0, column=0, sticky='w')
        self.entry = tk.Entry(frm, width=30)
        self.entry.grid(row=0, column=1, padx=6)

        tk.Label(frm, text="Tipe input:").grid(row=1, column=0, sticky='w', pady=6)
        self.type_var = tk.StringVar(value="decimal")
        choices = [("Desimal", "decimal"), ("Biner", "binary"), ("Oktal", "octal"), ("Heksadesimal", "hex")]
        for i, (lbl, val) in enumerate(choices):
            tk.Radiobutton(frm, text=lbl, variable=self.type_var, value=val).grid(row=1, column=1+i, sticky='w')

        tk.Button(self, text="Konversi", command=self.run_conversion).pack(anchor='w', pady=8)

    def run_conversion(self):
        val = self.entry.get().strip()
        t = self.type_var.get()
        try:
            if t == "decimal":
                n = int(val)
            elif t == "binary":
                n = int(val, 2)
            elif t == "octal":
                n = int(val, 8)
            else:
                n = int(val, 16)
        except:
            messagebox.showerror("Error", "Input tidak valid untuk tipe yang dipilih.")
            return

        b = bin(n)[2:]
        o = oct(n)[2:]
        h = hex(n)[2:].upper()
        out = f"Input ({t}) -> Desimal: {n}\nBiner: {b}\nOktal: {o}\nHeksadesimal: {h}"
        self.ctrl.write_output(out, clear=True)



class FramePermutasi(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller

        tk.Label(self, text="Permutasi", font=("Arial", 12, "bold")).pack(anchor='w', pady=6)

        frm = tk.Frame(self)
        frm.pack(anchor='w', pady=4)

        tk.Label(frm, text="Elemen (pisah spasi): ").grid(row=0, column=0, sticky='w')
        self.entry_elems = tk.Entry(frm, width=40)
        self.entry_elems.grid(row=0, column=1, padx=6)

        tk.Label(frm, text="k untuk permutasi sebagian (kosong = penuh): ").grid(row=1, column=0, sticky='w', pady=6)
        self.entry_k = tk.Entry(frm, width=10)
        self.entry_k.grid(row=1, column=1, sticky='w', padx=6)

        tk.Button(self, text="Hitung Permutasi", command=self.run_perm).pack(anchor='w', pady=8)

    def run_perm(self):
        data = self.entry_elems.get().strip().split()
        ktxt = self.entry_k.get().strip()
        try:
            if ktxt == "":
                perms = list(permutations(data))
            else:
                k = int(ktxt)
                perms = list(permutations(data, k))
        except:
            messagebox.showerror("Error", "Masukkan data dan k dengan benar.")
            return

        out_lines = [", ".join(p) for p in perms]
        header = f"Permutasi (n={len(data)}" + (f", k={ktxt}" if ktxt else "") + f") - total: {len(out_lines)}"
        self.ctrl.write_output(header + "\n" + "\n".join(out_lines), clear=True)



class FrameKombinasi(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller

        tk.Label(self, text="Kombinasi", font=("Arial", 12, "bold")).pack(anchor='w', pady=6)

        frm = tk.Frame(self)
        frm.pack(anchor='w', pady=4)
        tk.Label(frm, text="Masukkan n (jumlah total): ").grid(row=0, column=0, sticky='w')
        self.entry_n = tk.Entry(frm, width=8)
        self.entry_n.grid(row=0, column=1, padx=6, sticky='w')

        tk.Label(frm, text="Masukkan r (dipilih): ").grid(row=1, column=0, sticky='w', pady=6)
        self.entry_r = tk.Entry(frm, width=8)
        self.entry_r.grid(row=1, column=1, padx=6, sticky='w')

        tk.Button(self, text="Hitung Kombinasi dan Inisial Huruf", command=self.run_comb).pack(anchor='w', pady=8)

    def run_comb(self):
        try:
            n = int(self.entry_n.get().strip())
            r = int(self.entry_r.get().strip())
            if r > n or n < 0 or r < 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Masukkan n dan r yang valid.")
            return

        hasil = math.comb(n, r)
        out = f"Jumlah kombinasi C({n}, {r}) = {hasil}"

        if n <= 26:
            huruf = [chr(65 + i) for i in range(n)]
            combs = list(combinations(huruf, r))
            out += "\nKombinasi huruf:"
            for c in combs:
                out += "\n" + "".join(c)
        else:
            out += "\n(Terlalu banyak huruf untuk ditampilkan)"
        self.ctrl.write_output(out, clear=True)


if __name__ == "__main__":
    app = Praktikum3App()
    app.mainloop()
