from cmath import sqrt


x = [int(input("x1: ")),int(input("x2: "))]
y = [int(input("y1: ")),int(input("y2: "))]
dist = sqrt(pow((x[1] - x[0]),2) + pow((y[1] - y[0]),2))
print(pow(dist,2))