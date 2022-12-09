class Person:
    def __init__(self):
        self.name = "Taro"

    def say(self):
        print(f"My name is {self.name}.")

a = Person()
a.say()
a.name = 'Jiro'
a.say()