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

## printing the data
y = ids
x = vds
max_p = []
for xi, yi in zip(x,y):
    p = xi*yi # getting the power
    max_p.append(float(p))
print(f'Po_max: {max(max_p)} W')
c = max_p.index(max(max_p))
print(f"Index of Po_max: {c}")
print(f"Ids[index]: {y[c]} A")
print(f"Vds[index]: {x[c]} V")
a = y[c]*x[c]
print(f"Vds[index]*Ids[index]: {a} W")


# plt.ylim(min(y),max(y))
# plt.xlim(min(x),max(x))
plt.plot(x,y)
plt.ylabel("Ids [A]")
plt.xlabel("Vds [V]")

plt.show()




















end = time()
print(f"{end-start} s.")