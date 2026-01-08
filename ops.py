import matplotlib.pyplot as plt

x = [(a-50)/10 for a in range(100)]
x.remove(1)
x.remove(-1)
to_plot = [
    [1/a for a in x[:49]] + [0] + [1/a for a in x[50:]],
    [-1/a for a in x[:49]] + [0] + [-1/a for a in x[50:]],
    [a/(1-a) for a in x],
    [a/(a-1) for a in x],
    [a/(a+1) for a in x],
    [a*(1-a) for a in x],
    [(a*a)/(1-a) for a in x],
    [(a*a)/(a-1) for a in x],
    [()]
]

labels = ['a/(1-a)', 'a/(a-1)', 'a*a/(1-a)', 'a*a/(a-1)', '1/a', '-1/a']
for i in range(len(x)):
    print('%s %s' % (i, x[i]), end=' ')
    for g in to_plot:
        print(g[i],end=' ')
    print()
for i in range(len(to_plot)):
    plt.plot(x, to_plot[i], label = labels[i])
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('ops')
plt.legend()
plt.show()