import tkinter as tk
from tkinter import messagebox

class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()

    def _format_text(self, text):
        return ''.join([c for c in text.upper() if c.isalpha()])

    def _generate_key(self, text):
        key = self.key
        if len(text) == len(key):
            return key
        else:
            return (key * (len(text) // len(key))) + key[:len(text) % len(key)]

    def encrypt(self, plaintext):
        plaintext = self._format_text(plaintext)
        key = self._generate_key(plaintext)
        ciphertext = ""
        detail = []
        for i in range(len(plaintext)):
            p = ord(plaintext[i]) - 65
            k = ord(key[i]) - 65
            c = (p + k) % 26
            cipher_char = chr(c + 65)
            ciphertext += cipher_char
            detail.append(f"{plaintext[i]} {key[i]} ({p}+{k})%26={c} -> {cipher_char}")
        return ciphertext, "\n".join(detail)

    def decrypt(self, ciphertext):
        ciphertext = self._format_text(ciphertext)
        key = self._generate_key(ciphertext)
        plaintext = ""
        detail = []
        for i in range(len(ciphertext)):
            c = ord(ciphertext[i]) - 65
            k = ord(key[i]) - 65
            p = (c - k + 26) % 26
            plain_char = chr(p + 65)
            plaintext += plain_char
            detail.append(f"{ciphertext[i]} {key[i]} ({c}-{k})%26={p} -> {plain_char}")
        return plaintext, "\n".join(detail)


class VigenereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vigenere Cipher (PBO Version)")
        self.root.geometry("600x500")

        self.lbl_key = tk.Label(root, text="Key:")
        self.lbl_key.pack()
        self.ent_key = tk.Entry(root, width=40)
        self.ent_key.pack(pady=5)

        self.lbl_text = tk.Label(root, text="Input Text:")
        self.lbl_text.pack()
        self.ent_text = tk.Entry(root, width=40)
        self.ent_text.pack(pady=5)

        self.btn_encrypt = tk.Button(root, text="Enkripsi", width=15, command=self.do_encrypt)
        self.btn_encrypt.pack(pady=5)

        self.btn_decrypt = tk.Button(root, text="Dekripsi", width=15, command=self.do_decrypt)
        self.btn_decrypt.pack(pady=5)

        self.lbl_result = tk.Label(root, text="Hasil:")
        self.lbl_result.pack()
        self.txt_result = tk.Text(root, width=70, height=10)
        self.txt_result.pack(pady=5)

        self.lbl_detail = tk.Label(root, text="Detail Proses:")
        self.lbl_detail.pack()
        self.txt_detail = tk.Text(root, width=70, height=10)
        self.txt_detail.pack(pady=5)

    def do_encrypt(self):
        key = self.ent_key.get()
        plaintext = self.ent_text.get()
        if not key or not plaintext:
            messagebox.showwarning("Peringatan", "Masukkan key dan teks terlebih dahulu!")
            return
        cipher = VigenereCipher(key)
        result, detail = cipher.encrypt(plaintext)
        self.txt_result.delete(1.0, tk.END)
        self.txt_result.insert(tk.END, result)
        self.txt_detail.delete(1.0, tk.END)
        self.txt_detail.insert(tk.END, detail)

    def do_decrypt(self):
        key = self.ent_key.get()
        ciphertext = self.ent_text.get()
        if not key or not ciphertext:
            messagebox.showwarning("Peringatan", "Masukkan key dan teks terlebih dahulu!")
            return
        cipher = VigenereCipher(key)
        result, detail = cipher.decrypt(ciphertext)
        self.txt_result.delete(1.0, tk.END)
        self.txt_result.insert(tk.END, result)
        self.txt_detail.delete(1.0, tk.END)
        self.txt_detail.insert(tk.END, detail)


if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereApp(root)
    root.mainloop()
