score = int(input("点数を入力: "))
if score >= 90:
    print("やったね")
    print("判定：優")
elif score >= 60:
    print("判定：可")
else:
    print("残念でした")