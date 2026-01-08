import matplotlib.pyplot as plt

x = []
y = []
auri = [(a-50)/10 for a in range(100)]
buri = [(a-70)/10 for a in range(100)]
for a in auri:
    for b in buri:
        sum = a + b
        x.append(sum)
        prod = a * b
        y.append(prod)
        print('%s + %s = %s vs %s = %s * %s' % (a, b, sum, prod, a, b))

plt.plot(auri*100, x, label='sums')
plt.plot(auri*100, y, label='prods')
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('*')
plt.legend()
plt.show()