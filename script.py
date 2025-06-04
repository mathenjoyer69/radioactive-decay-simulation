import csv
import matplotlib.pyplot as plt
import numpy as np

def read_data(path):
    Rb_Sr_list = []
    Sr_Sr_list = []
    with open(path) as csvfile:
        data = list(csv.reader(csvfile, delimiter=','))
    for i in range(2,len(data),2):
        Rb_Sr_list.append(float(data[i][0]))
        Sr_Sr_list.append(float(data[i][1]))
    return Rb_Sr_list, Sr_Sr_list

def plot_best_fit_line(x_list, y_list, name):
    m, b = np.polyfit(np.array(x_list), np.array(y_list), 1)
    y_pred = np.array(x_list) * m + b
    plt.plot(x_list,y_pred,'--')

    plt.plot(x_list,y_list,'o',label=f"y={m:.4f}x+{b:.3f}")
    plt.xlabel('$^{87}Rb/^{87}Sr$')
    plt.ylabel('$^{87}Sr/^{86}Sr$')
    plt.title(name)
    plt.legend()

    plt.savefig(f"C:/Users/ariel/PycharmProjects/phat-alpha-decay-simulation/images/{name}.png",format='png')
    plt.cla()
    plt.close()
    return m,b

def calc_age(slope, Lambda):
    return np.log(slope+1)/Lambda

def isochron_graph(initial_elements, decay_constant):
    Rb_Sr_range = np.linspace(0, 1.0, 5)
    time_slices = [0, 1e9, 2e9, 3e9, 4e9,4.5e9]

    fig, ax = plt.subplots(figsize=(11, 8))

    Sr_ratios_per_time = []

    for t in time_slices:
        Sr_ratios = initial_elements + Rb_Sr_range * (np.exp(decay_constant * t) - 1)
        Sr_ratios_per_time.append(Sr_ratios)
        ax.plot(Rb_Sr_range, Sr_ratios)
        ax.plot(Rb_Sr_range, Sr_ratios)

    for i in range(len(time_slices) - 1):
        for j in range(len(Rb_Sr_range)):
            x = Rb_Sr_range[j]
            y_start = Sr_ratios_per_time[i][j]
            y_end = Sr_ratios_per_time[i + 1][j]
            ax.annotate('', xy=(float(x), float(y_end)), xytext=(float(x), float(y_start)), arrowprops=dict(arrowstyle='->', color='gray'))
            mid_y = (y_start + y_end) / 2
            ax.text(float(x) + 0.01, float(mid_y), f'{(time_slices[i + 1] - time_slices[i]) / 1e9:.1f} Gyr', fontsize=8, color='gray')

    ax.set_xlabel(r"$^{87}$Rb/$^{86}$Sr")
    ax.set_ylabel(r"$^{87}$Sr/$^{86}$Sr")
    ax.set_title("Isochron Evolution Over Time")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(initial_elements, initial_elements + 0.05)
    ax.grid(True)
    plt.show()

directories = ["csv_files/Abee.csv", "csv_files/Jelica.csv", "csv_files/Olivenza.csv", "csv_files/Saint-Sauveur.csv", "csv_files/Soko-Banja.csv"]
names=["Abee", "Jelica", "Olivenza", "Saint-Sauver", "Soko-Banja"]

ages = []
sr87_sr86_list = []
lambda_r = 1.42e-11
for i in range(len(directories)):
     Rb_Sr_list,Sr_Sr_list=read_data(directories[i])
     m, _ = plot_best_fit_line(Rb_Sr_list,Sr_Sr_list,names[i])
     ages.append(calc_age(m, lambda_r))
     sr87_sr86_list.append(sum(Sr_Sr_list)/len(Sr_Sr_list))

print(f"the average age is: {np.average(ages)/1e9:.4f} Billion Years")

Sr87_Sr86_average = sum(sr87_sr86_list)/len(sr87_sr86_list)
isochron_graph(Sr87_Sr86_average, lambda_r)