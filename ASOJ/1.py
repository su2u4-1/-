a = input()
for i in range(0, len(a) - 2):
    if a[i : i + 3] == "AUG":
        s = i
        break
for i in range(s, len(a), 3):
    if a[i : i + 3] == "UAA" or a[i : i + 3] == "UAG" or a[i : i + 3] == "UGA":
        e = i
        break
print(int((e - s) / 3))
