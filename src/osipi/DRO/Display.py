from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_mri(slices, mode="time", slice_index=0, time_index=0):
    fig, ax = plt.subplots()
    if mode == "time":
        frames = slices.shape[-1]

        def init():
            ax.imshow(slices[:, :, slice_index, 0], cmap="gray")
            ax.set_title(f"Slice: {slice_index}, Time: 0")

        def animate(t):
            ax.clear()
            ax.imshow(slices[:, :, slice_index, t], cmap="gray")
            ax.set_title(f"Slice: {slice_index}, Time: {t}")

    elif mode == "slice":
        frames = slices.shape[2]

        def init():
            ax.imshow(slices[:, :, 0, time_index], cmap="gray")
            ax.set_title(f"Slice: 0, Time: {time_index}")

        def animate(z):
            ax.clear()
            ax.imshow(slices[:, :, z, time_index], cmap="gray")
            ax.set_title(f"Slice: {z}, Time: {time_index}")

    anim = FuncAnimation(
        fig=fig, func=animate, frames=frames, init_func=init, interval=10000, blit=False
    )
    plt.show()
    return anim
