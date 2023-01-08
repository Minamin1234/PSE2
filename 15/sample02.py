with open("./alice_chap1.txt", "r") as file:
    data = file.read()
words = data.split()
print("単語数:", len(words))
