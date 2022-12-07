def bmi (height, weight):
    height_master = 0.01 * height
    return weight / height_master ** 2

while True:
    h = float(input("身長 [cm]: "))
    w = float(input("体重[kg]: "))
    b = bmi(height=h, weight=w)
    print(f"BMI: {b:.1f}")