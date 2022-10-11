nums = []
sum = 0
for i in range(10):
    num = int(input(f"値{i+1}: "))
    #num = int(input("値" + str(i+1) + ": "))
    nums.append(num)
    sum += num
print(f"合計: {sum}")
