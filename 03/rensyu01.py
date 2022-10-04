import math
xy1 = [int(input("x1: ")),int(input("y1: "))]
xy2 = [int(input("x2: ")),int(input("y2: "))]
dist = math.sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2)
print(dist**2)