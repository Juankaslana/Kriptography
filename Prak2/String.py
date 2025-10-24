text = input("Input Text: ")

print("Teks dari kiri:")
for i in range(1, len(text) + 1):
    print(text[:i])

print("\nTeks dari kanan:")
for i in range(1, len(text) + 1):
    print(text[-i:])

print("\nTeks dari tengah:")
middle = len(text) // 2
for i in range(middle + 1):
    start = middle - i
    end = middle + i + 1
    print(text[start:end])

print("\n=== SEKIAN DAN TERIMAKASIH ===")
