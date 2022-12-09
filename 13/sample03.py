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

class Student(Person):
    def __init__(self, name, school, grade):
        super().__init__(name)
        self.school = school
        self.grade = grade
    
    def display_status(self):
        super().display_status()
        print("school", self.school)
        print("grade", self.grade)

hanako = Student("Hanako", "OECU", 2)
hanako.display_status()
hanako.buy("pen", 50)
hanako.display_status()