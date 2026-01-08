spread = dict()
spread[0] = [1]
base = 2
for i in range(100):
    c = i
    pow = 0
    while c % base == 0 and c != 0:
        c = int(c / base)
        pow += 1
    if c == 1:
        spread[pow] = [c]
    else:
        spread[pow].append(c)
for key in spread.keys():
    print('%s %s' % (key, spread[key]))
