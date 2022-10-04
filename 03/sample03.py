from random import sample


sample_list = []

sample_list.append(input("1つ目を入力"))
sample_list.append(input("2つ目を入力"))
sample_list.append(input("3つ目を入力"))

for i in range(3):
    print(i,"番目: ",sample_list[i])