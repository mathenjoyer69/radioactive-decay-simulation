import numpy as np
import matplotlib.pyplot as plt

def isochron_graph(initial_elements, decay_constant):
    Rb_Sr_range = np.linspace(0, 1.0, 5)
    time_slices = [0, 1e9, 2e9, 3e9, 4e9,4.5e9]

    fig, ax = plt.subplots(figsize=(11, 8))

    Sr_ratios_per_time = []

    for t in time_slices:
        Sr_ratios = initial_elements + Rb_Sr_range * (np.exp(decay_constant * t) - 1)
        Sr_ratios_per_time.append(Sr_ratios)
        ax.plot(Rb_Sr_range, Sr_ratios, lw=1)
        ax.plot(Rb_Sr_range, Sr_ratios)

    for i in range(len(time_slices) - 1):
        for j in range(len(Rb_Sr_range)):
            x = Rb_Sr_range[j]
            y_start = Sr_ratios_per_time[i][j]
            y_end = Sr_ratios_per_time[i + 1][j]
            ax.annotate('', xy=(float(x), y_end), xytext=(float(x), y_start), arrowprops=dict(arrowstyle='->', color='gray'))
            mid_y = (y_start + y_end) / 2
            ax.text(float(x) + 0.01, float(mid_y), f'{(time_slices[i + 1] - time_slices[i]) / 1e9:.1f} Gyr', fontsize=8, color='gray')

    ax.set_xlabel(r"$^{87}$Rb/$^{86}$Sr")
    ax.set_ylabel(r"$^{87}$Sr/$^{86}$Sr")
    ax.set_title("Isochron Evolution Over Time")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(initial_elements, initial_elements + 0.05)
    ax.grid(True)
    plt.show()

lambda_r = 1.42e-11
Sr87_Sr86_initial = 0.69885
isochron_graph(Sr87_Sr86_initial, lambda_r)