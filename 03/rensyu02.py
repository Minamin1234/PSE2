nums = []
sum = 0

for i in range(10):
    num = int(input(f"{i+1}: "))
    nums.append(num)
    sum += num

print(f"入力された値: {nums}")
print(f"平均値: {int(sum / 10)}")