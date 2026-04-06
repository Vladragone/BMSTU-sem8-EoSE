import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def create_factor_analysis_plot(root, factors, pm_values, tdev_values):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    factor_names = factors
    x = range(len(factor_names))

    ax.bar(x, pm_values, width=0.4, label='PM')
    ax.bar([i + 0.4 for i in x], tdev_values, width=0.4, label='TDEV')

    ax.set_xticks([i + 0.2 for i in x])
    ax.set_xticklabels(factor_names)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    return canvas.get_tk_widget()