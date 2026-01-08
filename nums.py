# importing the required module
import matplotlib.pyplot as plt
 
def f(x):
    if x % 2 ==0:
        x = int(x/2)
    else:
        x = int((x - 1) / 2)
    return x

def p(x):
    l = []
    c = x
    loops = 0
    while c not in l and loops < 1000:
        l.append(c)
        c = f(c)
        loops += 1
    print('%s %s %s' % (l[-1], l, loops))
    return l

# x axis values
i = [a-100 for a in range(200)]
# corresponding y axis values
x = []
y = []
for z in i:
    c = p(z)
    x.extend(len(c) * [z])
    y.extend(c)
# plotting the points 
plt.plot(x, y, ':')
 
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
 
# giving a title to my graph
plt.title('My first graph!')
 
# function to show the plot
plt.show()
