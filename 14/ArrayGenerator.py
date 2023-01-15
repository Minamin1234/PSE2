import sys
x_ = int(sys.argv[1])
y_ = int(sys.argv[2])
content = sys.argv[3]
cnt = len(content)
ARRAY_BEGIN = "["
ARRAY_END = "]"
SPRT = ","
result = ""

result += ARRAY_BEGIN + "\n"
for y in range(y_):
    result += "\t" + ARRAY_BEGIN
    for x in range(x_):
        result += f"{content:{cnt}}{SPRT} "
        if x == (x_-1):
            result = result.rstrip(SPRT + " ")
            pass
        pass
    result += ARRAY_END + SPRT + "\n"
    if y == (y_ - 1):
        result = result.rstrip(SPRT)
        pass
    pass
result += ARRAY_END
print(result)
