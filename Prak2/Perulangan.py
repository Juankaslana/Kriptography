for i in range(1, 6):
    print("Angka:", i)

countdown = 5
while countdown > 0:
    print("Hitung mundur:", countdown)
    countdown -= 1

for i in range(1, 10):
    if i == 5:
        break
    elif i % 2 == 0:
        continue
    print(i)

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
