bestscores = {}
with open("./bestscores.txt", "r") as file:
    for line in file:
        words = line.split()
        if len(words) >= 2:
            bestscores[words[0]] = int(words[1])

for i in sorted(bestscores.items(), key=lambda x: x[1], reverse=True):
    print(f"{i[0]:10} {i[1]:3}")