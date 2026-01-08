import matplotlib.pyplot as plt
 
def get_x(x):
    c = x
    if c % 2 == 1:
        c = 3*x+1
    else:
        while c % 2 == 0 and c != 0:
            c = c / 2
    return c




step = [a for a in range(1000)]
print(step)
rot = 0
coords = dict()
for steps in range(100):
    c = step.copy()
    step = [get_x(a) for a in step]
    for i in range(len(c)):
        if rot == 0:
            x = c[i]
            y = step[i]
        elif rot == 90:
            x = step[i]
            y = c[i]
            x = x * -1
        elif rot == 180:
            x = c[i]
            y = step[i]
            x = x * -1
            y = y * -1
        elif rot == 270:
            x = step[i]
            y = c[i]
            y = y * -1
        if i not in coords:
            coords[i] = [(x,y)]
        else:
            coords[i].append((x,y))
    rot = (rot + 90) % 360
for i in range(len(coords)):
    print('%s %s' % (i,coords[i]))

#for i in range(len(coords)):
#draw falling and rising in different colors
i = 983
all_x = []
all_y = []
for x,y in coords[i]:
    all_x.append(x)
    all_y.append(y)
plt.plot(all_x, all_y)
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('collatz')
plt.show()