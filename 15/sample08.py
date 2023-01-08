def print_ranking():
    for i in sorted(bestscores.items(), key=lambda x: x[1], reverse=True):
        print(f'{i[0]:10} {i[1]:3}')


bestscores = {}
with open('PSE2_15/bestscores.txt', 'r') as file:
    for line in file:
        words = line.split()
        if len(words) >= 2:
            bestscores[words[0]] = int(words[1])

print('開始前ランキング:')
print_ranking()

while True:
    name = input('名前: ')
    if name == '':  # 入力された名前が空ならばループを抜ける
        break
    score = int(input('スコア: '))
    if name in bestscores:
        print(f'{name}は登録済み')
        if score > bestscores[name]:
            print('最高点更新')
            bestscores[name] = score
        else:
            print('残念')
    else:
        print(f'{name}は新規')
        bestscores[name] = score

print('終了後ランキング:')
print_ranking()

try:
    with open("./bestscores.txt", "w") as file:
        for i in bestscores.items():
            file.write(f"{i[0]}\t{i[1]}\n")
except OSError as e:
    print("ベストスコアのファイルがない")
