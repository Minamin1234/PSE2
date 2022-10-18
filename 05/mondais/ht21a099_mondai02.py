nums = []
mx = 0
mn = int(input(f"値{1}: "))
for i in range(9):
    n = int(input(f"値{i+2}: "))
    nums.append(n)
    mx = max(mx,n)
    mn = min(mn,n)

print(f"最大値: {mx}")
print(f"最小値: {mn}")
#print(f"最大値: {max(nums)}")
#print(f"最小値: {min(nums)}")