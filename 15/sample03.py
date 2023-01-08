print("開始")
with open("./kuku.txt", "w") as file:
    for i in range(1, 10):
        for j in range(1, 10):
            file.write(f"{i*j:3}")
        file.write("\n")
print("終了")