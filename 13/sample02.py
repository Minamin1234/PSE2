class Person:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.items = []

    def display_status(self):
        print("------------")
        print("name:", self.name)
        print("money:", self.money)
        print("items", self.items)

    def buy(self, item, price):
        self.money -= price
        self.items.append(item)

taro = Person("taro")
taro.display_status()
taro.buy("milk", 50)
taro.buy("apple", 100)
taro.display_status()