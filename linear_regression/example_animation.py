import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

beta = 12
x = np.arange(0, 100, 1)
(line,) = ax.plot(x, np.sin(x))


def init():  # only required for blitting to give a clean slate.
    line.set_ydata([np.nan] * len(x))
    return (line,)


def animate(i):
    line.set_ydata(np.sin(x + i / 100))  # update the data.
    return (line,)


# ani = animation.FuncAnimation(
#     fig, animate, init_func=init, interval=2, blit=True, save_count=50
# )
# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)


for delta in range(1000):
    y = list(map(lambda x: x * delta + beta, x))
    ax.plot(x, y)
#     line.set_ydata(y)
#     plt.show()

plt.show()
