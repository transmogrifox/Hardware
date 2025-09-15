import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib.animation import FFMpegWriter

# Fixing random state for reproducibility
np.random.seed(19680801)


metadata = dict(title='Jittering line stretch', artist='The Transmogrifox',
                comment='This is the comment')
writer = FFMpegWriter(fps=15, metadata=metadata)

fig = plt.figure()
l, = plt.plot([], [], 'k-o')

plt.xlim(-5, 5)
plt.ylim(-5, 5)

x0, y0 = 0, 0
n = 0
with writer.saving(fig, "writer_test.mp4", 100):
    for i in range(100):
        n += 1
        x0 += 0.25 * np.random.randn()
        y0 += 0.1 * np.random.randn()
        x1 = x0+0.05*n
        y1 = y0 + y0*n*0.025
        l.set_data([x0 - 0.035*n,x1], [y0,y1])
        writer.grab_frame()
