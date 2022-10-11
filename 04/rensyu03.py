def postTaxPrice(price):
    ans = price * 1.10
    return ans
price = int(input("金額を入力： "))
print(f"税込： {postTaxPrice(price)}円")