import matplotlib.pyplot as plt
import math

data = {}
c=['b','g','r','c','m','y']
for i in range(6):
    data[2**(i+1)] = [([],[]) for _ in range(i+1)]

with open("./results.txt", 'r') as file:
    for line in file:
        parts = line.split()
        if len(parts) != 5:
            continue
        tasks = int(parts[0])
        messageSize = int(parts[1])
        shifts = int(parts[2])
        time = float(parts[3])
        data[tasks][int(math.log2(shifts))][0].append(messageSize*2)
        data[tasks][int(math.log2(shifts))][1].append(time)

plt.figure(figsize=(10, 6))
plt.yscale("log")
plt.xscale("log")
plt.title(f"Time vs Message Size")
plt.xlabel('Message Size (bytes)')
plt.ylabel('Time (seconds)')
plt.grid(True)
i = 0
for tasks in data:
    plt.plot(data[tasks][0][0], data[tasks][0][1], marker='o', color=c[i], linestyle='-', label=f"{tasks} tasks")
    i += 1
plt.legend()
plt.savefig("./Q4_plot.png")
