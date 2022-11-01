import sklearn.datasets

digits = sklearn.datasets.load_digits()

print(f"データの個数= {len(digits.images)}")
print(f"画像データ= {digits.images[0]}")
print(f"何の数字か= {digits.target[0]}")