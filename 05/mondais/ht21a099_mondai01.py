n = int(input("整数を入力: "))
is_ = " は,"
signed = "負の"
unsigned = "正の"
odd = "奇数"
even = "偶数"

if n >= 0:
    if n % 2 == 0:
        print(f"{n}{is_}{unsigned}{even}")
    else:
        print(f"{n}{is_}{unsigned}{odd}")
else:
    if n % 2 == 0:
        print(f"{n}{is_}{signed}{even}")
    else:
        print(f"{n}{is_}{signed}{odd}")