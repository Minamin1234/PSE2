def Total(cnt):
    if cnt >= 30:
        return (100 * cnt) * 0.8
    elif cnt >= 10:
        return (100 * cnt) * 0.9
    return 100 * cnt

print(Total(5))
print(Total(10))
print(Total(15))
print(Total(35))
