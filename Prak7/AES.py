import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import math

# ================= AES TABLES (SBOX as 16x16) and RCON =================
SBOX = [
[0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
[0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
[0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
[0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
[0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
[0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
[0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
[0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
[0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
[0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
[0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
[0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
[0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
[0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
[0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
[0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]
]

# Rcon (index start at 1)
RCON = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

# ================= Utility funcs =================
def text_to_bytes(text):
    return text.encode('utf-8')

def bytes_to_hex(b):
    return ''.join(f"{x:02X}" for x in b)

def state_to_hex(state):
    arr = []
    for c in range(4):
        for r in range(4):
            arr.append(state[r][c])
    return ''.join(f"{x:02X}" for x in arr)

def hex_bytes_to_str(bytes_list):
    return ' '.join(f"{x:02X}" for x in bytes_list)

def get_sbox_val(byte):
    return SBOX[byte >> 4][byte & 0x0F]

def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

# PKCS7 pad/unpad for block size 16
def pkcs7_pad(data_bytes):
    pad_len = 16 - (len(data_bytes) % 16)
    return data_bytes + bytes([pad_len])*pad_len

def pkcs7_unpad(data_bytes):
    if not data_bytes: return data_bytes
    pad = data_bytes[-1]
    return data_bytes[:-pad]

# ================= AES core primitives =================
def sub_bytes(state, trace_lines, label_prefix=""):
    # state: 4x4
    # Append detailed mapping: original byte -> sbox(row,col) -> result
    trace_lines.append(f"{label_prefix}SubBytes mapping (byte -> SBOX[row,col] -> result):")
    for r in range(4):
        row_map = []
        for c in range(4):
            orig = state[r][c]
            row_idx = orig >> 4
            col_idx = orig & 0x0F
            res = get_sbox_val(orig)
            row_map.append(f"{orig:02X}->{row_idx:X},{col_idx:X}->{res:02X}")
            state[r][c] = res
        trace_lines.append("  Row{}: ".format(r) + "  ".join(row_map))
    trace_lines.append("  After SubBytes state: " + state_to_hex(state))

def shift_rows(state, trace_lines):
    trace_lines.append("ShiftRows (before): " + state_to_hex(state))
    # Represent rows for clarity
    rows_before = [[state[r][c] for c in range(4)] for r in range(4)]
    trace_lines.append("  Rows before:")
    for r in range(4):
        trace_lines.append("    Row{}: {}".format(r, hex_bytes_to_str(rows_before[r])))
    # perform shift
    state[1] = state[1][1:]+state[1][:1]
    state[2] = state[2][2:]+state[2][:2]
    state[3] = state[3][3:]+state[3][:3]
    rows_after = [[state[r][c] for c in range(4)] for r in range(4)]
    trace_lines.append("  Rows after:")
    for r in range(4):
        trace_lines.append("    Row{}: {}".format(r, hex_bytes_to_str(rows_after[r])))
    trace_lines.append("  After ShiftRows state: " + state_to_hex(state))

def mix_single_column_with_detail(col, trace_lines, col_index):
    # col: list of 4 ints (a0,a1,a2,a3)
    a0,a1,a2,a3 = col
    trace_lines.append(f"[MixColumns - Kolom {col_index}]")
    trace_lines.append(f"Input kolom: {a0:02X} {a1:02X} {a2:02X} {a3:02X}\n")

    # 02·a0
    xt_a0 = xtime(a0)
    trace_lines.append(f"02·{a0:02X}:")
    trace_lines.append(f"  xtime({a0:02X}) = {xt_a0:02X}\n")

    # 03·a1 = xtime(a1) XOR a1
    xt_a1 = xtime(a1)
    mul3_a1 = xt_a1 ^ a1
    trace_lines.append(f"03·{a1:02X}:")
    trace_lines.append(f"  xtime({a1:02X}) = {xt_a1:02X}")
    trace_lines.append(f"  {xt_a1:02X} XOR {a1:02X} = {mul3_a1:02X}\n")

    # 01·a2
    trace_lines.append(f"01·{a2:02X}:")
    trace_lines.append(f"  = {a2:02X}\n")

    # 01·a3
    trace_lines.append(f"01·{a3:02X}:")
    trace_lines.append(f"  = {a3:02X}\n")

    # compute b0 = 02·a0 XOR 03·a1 XOR 01·a2 XOR 01·a3
    b0 = xt_a0 ^ mul3_a1 ^ a2 ^ a3
    trace_lines.append("XOR total for byte0:")
    xs = [(xt_a0, f"{xt_a0:02X}"), (mul3_a1, f"{mul3_a1:02X}"), (a2, f"{a2:02X}"), (a3, f"{a3:02X}")]
    cur = xs[0][0]
    trace_lines.append(f"  {xs[0][1]}")
    for val, sval in xs[1:]:
        cur = cur ^ val
        trace_lines.append(f"  XOR {sval} = {cur:02X}")
    trace_lines.append(f"  Result byte0 = {b0:02X}\n")

    # Now for b1: a0 XOR 02·a1 XOR 03·a2 XOR 01·a3
    # compute 02·a1 already as xt_a1, 03·a2 = xtime(a2) XOR a2
    xt_a2 = xtime(a2)
    mul3_a2 = xt_a2 ^ a2
    b1 = a0 ^ xt_a1 ^ mul3_a2 ^ a3
    trace_lines.append(f"02·{a1:02X} (used in byte1) = {xt_a1:02X}")
    trace_lines.append(f"03·{a2:02X}:")
    trace_lines.append(f"  xtime({a2:02X}) = {xt_a2:02X}")
    trace_lines.append(f"  {xt_a2:02X} XOR {a2:02X} = {mul3_a2:02X}")
    trace_lines.append("XOR total for byte1:")
    xs = [(a0, f"{a0:02X}"), (xt_a1, f"{xt_a1:02X}"), (mul3_a2, f"{mul3_a2:02X}"), (a3, f"{a3:02X}")]
    cur = xs[0][0]
    trace_lines.append(f"  {xs[0][1]}")
    for val, sval in xs[1:]:
        cur = cur ^ val
        trace_lines.append(f"  XOR {sval} = {cur:02X}")
    trace_lines.append(f"  Result byte1 = {b1:02X}\n")

    # b2 = a0 XOR a1 XOR 02·a2 XOR 03·a3
    xt_a3 = xtime(a3)
    mul3_a3 = xt_a3 ^ a3
    b2 = a0 ^ a1 ^ xt_a2 ^ mul3_a3
    trace_lines.append(f"02·{a2:02X} (used in byte2) = {xt_a2:02X}")
    trace_lines.append(f"03·{a3:02X}:")
    trace_lines.append(f"  xtime({a3:02X}) = {xt_a3:02X}")
    trace_lines.append(f"  {xt_a3:02X} XOR {a3:02X} = {mul3_a3:02X}")
    trace_lines.append("XOR total for byte2:")
    xs = [(a0, f"{a0:02X}"), (a1, f"{a1:02X}"), (xt_a2, f"{xt_a2:02X}"), (mul3_a3, f"{mul3_a3:02X}")]
    cur = xs[0][0]
    trace_lines.append(f"  {xs[0][1]}")
    for val, sval in xs[1:]:
        cur = cur ^ val
        trace_lines.append(f"  XOR {sval} = {cur:02X}")
    trace_lines.append(f"  Result byte2 = {b2:02X}\n")

    # b3 = 03·a0 XOR a1 XOR a2 XOR 02·a3
    mul3_a0 = xt_a0 ^ a0
    b3 = mul3_a0 ^ a1 ^ a2 ^ xt_a3
    trace_lines.append(f"03·{a0:02X} = {xt_a0:02X} XOR {a0:02X} = {mul3_a0:02X}")
    trace_lines.append(f"02·{a3:02X} = {xt_a3:02X}")
    trace_lines.append("XOR total for byte3:")
    xs = [(mul3_a0, f"{mul3_a0:02X}"), (a1, f"{a1:02X}"), (a2, f"{a2:02X}"), (xt_a3, f"{xt_a3:02X}")]
    cur = xs[0][0]
    trace_lines.append(f"  {xs[0][1]}")
    for val, sval in xs[1:]:
        cur = cur ^ val
        trace_lines.append(f"  XOR {sval} = {cur:02X}")
    trace_lines.append(f"  Result byte3 = {b3:02X}\n")

    return [b0 & 0xFF, b1 & 0xFF, b2 & 0xFF, b3 & 0xFF]

def mix_columns_with_detail(state, trace_lines):
    # for each column 0..3
    trace_lines.append("MixColumns (detail GF(2^8) - FORMAT B):")
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        out_col = mix_single_column_with_detail(col, trace_lines, c)
        for r in range(4):
            state[r][c] = out_col[r]
    trace_lines.append("After MixColumns state: " + state_to_hex(state))

def add_round_key_with_detail(state, round_key, trace_lines, round_idx):
    trace_lines.append(f"AddRoundKey (Round {round_idx}) - byte XOR detail:")
    # round_key as 4x4
    for r in range(4):
        line = []
        for c in range(4):
            sb = state[r][c]
            rk = round_key[r][c]
            res = sb ^ rk
            line.append(f"{sb:02X} XOR {rk:02X} = {res:02X}")
            state[r][c] = res
        trace_lines.append("  " + "  ".join(line))
    trace_lines.append(f"After AddRoundKey({round_idx}) state: {state_to_hex(state)}")

# ================= Key expansion =================
def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [get_sbox_val(b) for b in word]

def key_expansion_from_keybytes_with_trace(key_bytes, trace_lines):
    w = [list(key_bytes[i:i+4]) for i in range(0,16,4)]
    trace_lines.append("Key Expansion detail (words W0..W43):")
    for idx, word in enumerate(w):
        trace_lines.append(f"  W{idx} = {' '.join(f'{b:02X}' for b in word)}")
    for i in range(4, 44):
        temp = w[i-1].copy()
        trace_lines.append(f"\nComputing W{i}: temp = W{i-1} = {' '.join(f'{b:02X}' for b in temp)}")
        if i % 4 == 0:
            trace_lines.append("  i % 4 == 0 -> apply RotWord, SubWord, XOR RCON")
            rot = rot_word(temp)
            trace_lines.append(f"  RotWord(temp) = {' '.join(f'{b:02X}' for b in rot)}")
            subw = sub_word(rot)
            trace_lines.append(f"  SubWord(Rot) = {' '.join(f'{b:02X}' for b in subw)}")
            subw[0] ^= RCON[i//4]
            trace_lines.append(f"  XOR RCON[{i//4}] = {RCON[i//4]:02X} -> temp = {' '.join(f'{b:02X}' for b in subw)}")
            temp = subw
        neww = [ (w[i-4][j] ^ temp[j]) & 0xFF for j in range(4) ]
        w.append(neww)
        trace_lines.append(f"  W{i} = W{i-4} XOR temp = {' '.join(f'{b:02X}' for b in neww)}")
    round_keys = []
    trace_lines.append("\nRound keys (as 16-byte hex each):")
    for r in range(11):
        block = w[r*4:(r+1)*4]
        rk = [[ block[col][row] for col in range(4) ] for row in range(4)]
        round_keys.append(rk)
        trace_lines.append(f"  RoundKey[{r}] = {state_to_hex(rk)}")
    return round_keys

# ================= AES encrypt single block with very detailed trace =================
def encrypt_block_trace_full(block_bytes, round_keys, trace_lines, block_index):
    trace_lines.append(f"\n--- BLOCK {block_index} TRACE ---")
    # build state column-major
    state = [[0]*4 for _ in range(4)]
    for i in range(16):
        state[i%4][i//4] = block_bytes[i]
    trace_lines.append("State (input) : " + state_to_hex(state))

    # Round 0 AddRoundKey (detail)
    trace_lines.append("RoundKey[0]    : " + state_to_hex(round_keys[0]))
    add_round_key_with_detail(state, round_keys[0], trace_lines, 0)

    # Rounds 1..9
    for r in range(1,10):
        trace_lines.append(f"\n--- ROUND {r} ---")
        sub_bytes(state, trace_lines, label_prefix="")
        shift_rows(state, trace_lines)
        mix_columns_with_detail(state, trace_lines)
        trace_lines.append("RoundKey[{}]    : ".format(r) + state_to_hex(round_keys[r]))
        add_round_key_with_detail(state, round_keys[r], trace_lines, r)

    # Final round 10 (no MixColumns)
    trace_lines.append("\n--- ROUND 10 (final) ---")
    sub_bytes(state, trace_lines)
    shift_rows(state, trace_lines)
    trace_lines.append("RoundKey[10]   : " + state_to_hex(round_keys[10]))
    add_round_key_with_detail(state, round_keys[10], trace_lines, 10)

    # output bytes from state (column-major)
    out_bytes = bytes(state[r][c] for c in range(4) for r in range(4))
    trace_lines.append("Output block (cipher hex): " + bytes_to_hex(out_bytes))
    return out_bytes

# ================= GUI and wiring =================
def run_aes_trace():
    text_in = entry_plain.get("1.0","end").rstrip("\n")
    key_text = entry_key.get().strip()

    # convert inputs
    pt_bytes = text_to_bytes(text_in)
    key_bytes = key_text.encode('utf-8')
    # normalize key to 16 bytes (pad with 0x00 or truncate)
    if len(key_bytes) < 16:
        key_bytes = key_bytes + b'\x00'*(16-len(key_bytes))
    else:
        key_bytes = key_bytes[:16]

    # pad plaintext PKCS7
    padded = pkcs7_pad(pt_bytes)
    blocks = [padded[i:i+16] for i in range(0,len(padded),16)]

    # prepare round keys WITH TRACE detail
    trace_lines = []
    trace_lines.append(f"Input text: {text_in}")
    trace_lines.append(f"Plaintext bytes (UTF-8): {bytes_to_hex(pt_bytes)}")
    trace_lines.append(f"Padded plaintext (PKCS7): {bytes_to_hex(padded)}\n")
    trace_lines.append(f"Key text: {key_text}")
    trace_lines.append(f"Key bytes (used, 16B): {bytes_to_hex(key_bytes)}\n")

    round_keys = key_expansion_from_keybytes_with_trace(key_bytes, trace_lines)

    ciphertext = b''
    for bi,blk in enumerate(blocks, start=1):
        trace_lines.append(f"\n=== BLOCK {bi} ===")
        trace_lines.append(f"Block bytes (hex): {bytes_to_hex(blk)}")
        out_blk = encrypt_block_trace_full(blk, round_keys, trace_lines, bi)
        ciphertext += out_blk

    trace_lines.append("\n=== FINAL CIPHERTEXT ===")
    trace_lines.append(bytes_to_hex(ciphertext))

    # display
    text_out.delete('1.0', tk.END)
    for line in trace_lines:
        text_out.insert(tk.END, line + "\n")

def export_trace_to_file():
    content = text_out.get("1.0","end")
    if not content.strip():
        messagebox.showinfo("Export", "Tidak ada trace untuk disimpan.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
    if not path:
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    messagebox.showinfo("Export", f"Trace disimpan ke {path}")

# Build GUI
root = tk.Tk()
root.title("AES-128 Detailed Trace (FORMAT B - GF(2^8) lengkap)")
root.geometry("1000x760")

lbl1 = tk.Label(root, text="Plaintext (ketik bebas, akan dikonversi ke bytes UTF-8):")
lbl1.pack(anchor='w', padx=8, pady=(8,0))
entry_plain = scrolledtext.ScrolledText(root, width=120, height=4)
entry_plain.pack(padx=8, pady=(0,6))
entry_plain.insert

lbl2 = tk.Label(root, text="Key (ketik text; dipad/truncate ke 16 bytes):")
lbl2.pack(anchor='w', padx=8, pady=(6,0))
entry_key = tk.Entry(root, width=80)
entry_key.pack(padx=8, pady=(0,6))
entry_key.insert

btn_frame = tk.Frame(root)
btn_frame.pack(padx=8, pady=6, anchor='w')

btn_run = tk.Button(btn_frame, text="Run AES-128 (detail lengkap FORMAT B)", command=run_aes_trace)
btn_run.grid(row=0, column=0, padx=4)

btn_export = tk.Button(btn_frame, text="Export trace to .txt", command=export_trace_to_file)
btn_export.grid(row=0, column=1, padx=4)

text_out = scrolledtext.ScrolledText(root, width=140, height=32)
text_out.pack(padx=8, pady=(6,12))

root.mainloop()
