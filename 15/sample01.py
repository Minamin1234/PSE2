dic = {"dog": "犬", "cat": "猫", "apple": "りんご", "hello": "こんにちは"}
while True:
    key = input("英単語: ")
    if key == "":
        print(dic)
    elif key in dic:
        print(f"{key}は「{dic[key]}」")
    else:
        print(f"{key}は知りません。教えてください。")
        value = input("日本語訳: ")
        dic[key] = value
        