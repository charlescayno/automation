import numpy as np
import matplotlib.pyplot as plt
from time import time, sleep
start = time()

# with open("waveform.txt") as f:
#     mylist = f.read().splitlines()
# data = []
# for n in mylist:
#     data.append(float(n))

# print()

# y = data
# x = list(range(len(data)))

# plt.ylim(min(y),max(y))
# plt.plot(x,y)

# plt.show()




with open('soa.csv') as f:
    lines = f.readlines()
    vds = [float(line.split(";")[0]) for line in lines]
    ids = [float(line.split(";")[1]) for line in lines]

# print(vds)
# print(ids)

print()

y = ids
x = vds
max_p = []
for xi, yi in zip(x,y):
    p = xi*yi
    max_p.append(float(p))
print(max(max_p))
c = max_p.index(max(max_p))
print(c)
print(y[c])
print(x[c])
a = y[c]*x[c]
print(a)


# plt.ylim(min(y),max(y))
# plt.xlim(min(x),max(x))
plt.plot(x,y)
# plt.plot(x,max_p)

plt.show()




















end = time()
print(f"{end-start} s.")