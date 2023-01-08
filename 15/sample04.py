bestscores = {}
with open("./bestscores.txt", "r") as file:
    for line in file:
        words = line.split()
        if len(words) >= 2:
            bestscores[words[0]] = int(words[1])

print(bestscores)