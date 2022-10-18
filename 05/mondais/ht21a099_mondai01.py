n = int(input("整数をご入力ください: "))
signed = "負の"
unsigned = "正の"
odd = "奇数"
even = "偶数"

if n >= 0:
    if n % 2 == 0:
        print(f"{unsigned}{even}")
    else:
        print(f"{unsigned}{odd}")
else:
    if n % 2 == 0:
        print(f"{signed}{even}")
    else:
        print(f"{signed}{odd}")