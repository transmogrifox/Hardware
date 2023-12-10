import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Get data
df = pd.read_csv('data_expo.txt', sep = '\t')

# Generate plot
fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1, constrained_layout=True)
fig.set_size_inches(16, 8)

ax1.plot(df["n"], df["y[n]"], "r")

ax1.set(xlabel='samples (n)', ylabel='Integer Counts',
       title='Decaying exponential\n(fixed point implementation)')
ax1.grid()

ax2.plot(df["n"], df["INTEG(y[n])"], "r")

ax2.set(xlabel='samples (n)', ylabel='Integer Counts',
       title='Accumulator offset')
ax2.grid()

fig.savefig("ExpoDecayPlot.png")
plt.show()