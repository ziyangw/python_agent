import matplotlib.pyplot as plt
import sys
file = sys.argv[1]
with open(file) as f:
    nums = [line.rstrip('\n') for line in f]

plt.plot(nums)
plt.show()
