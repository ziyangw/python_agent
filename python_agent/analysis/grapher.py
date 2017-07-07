import matplotlib.pyplot as plt
import sys
times_files = sys.argv[0]
with open(times_files) as f:
    times = [line.rstrip('\n') for line in open('filename')]

plt.plot(times)
plt.ylabel('ms')
plt.show()
