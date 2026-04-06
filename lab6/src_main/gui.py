import tkinter as tk
from tkinter import ttk
from cocomo import *
from plots import *


class COCOMOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COCOMO Calculator")

        # Переменные по умолчанию
        self.cocomo_type = tk.StringVar(value="semi-detached")
        self.size = tk.DoubleVar(value=55.0)
        self.factors = {
            "RELY": tk.DoubleVar(value=1.0),
            "DATA": tk.DoubleVar(value=1.08),
            "CPLX": tk.DoubleVar(value=1.0),
            "TIME": tk.DoubleVar(value=1.0),
            "ACAP": tk.DoubleVar(value=0.86),
            "PCAP": tk.DoubleVar(value=1.0),
            "MODP": tk.DoubleVar(value=1.0),
            "TOOL": tk.DoubleVar(value=1.0)
        }

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack()

        # Выбор типа проекта
        ttk.Label(main_frame, text="Project Type:").grid(row=0, column=0)
        ttk.Combobox(main_frame, textvariable=self.cocomo_type,
                     values=["organic", "semi-detached", "embedded"]).grid(row=0, column=1)

        # Ввод размера
        ttk.Label(main_frame, text="Size (KLOC):").grid(row=1, column=0)
        ttk.Entry(main_frame, textvariable=self.size).grid(row=1, column=1)

        # Драйверы затрат
        row = 2
        for factor in self.factors:
            ttk.Label(main_frame, text=f"{factor}:").grid(row=row, column=0)
            ttk.Combobox(main_frame, textvariable=self.factors[factor],
                         values=[0.75, 0.88, 1.0, 1.15, 1.40]).grid(row=row, column=1)
            row += 1

        # Кнопка расчета
        ttk.Button(main_frame, text="Calculate", command=self.calculate).grid(row=row, column=0, columnspan=2)

    def calculate(self):
        # Расчет EAF
        factors = {k: v.get() for k, v in self.factors.items()}
        eaf = get_eaf(factors)

        # Основные расчеты
        pm = calculate_pm(self.cocomo_type.get(), self.size.get(), eaf)
        tdev = calculate_tdev(self.cocomo_type.get(), pm)

        # Вывод результатов
        result_window = tk.Toplevel(self.root)
        ttk.Label(result_window, text=f"PM: {pm:.2f} чел-мес").pack()
        ttk.Label(result_window, text=f"TDEV: {tdev:.2f} мес").pack()

        # Графики
        plot_frame = ttk.Frame(result_window)
        plot_frame.pack()

        # Анализ факторов
        factors_analysis = ["MODP", "TOOL", "ACAP", "PCAP"]
        pm_values = []
        tdev_values = []
        for factor in factors_analysis:
            original = factors[factor]
            factors[factor] = 1.24  # Очень низкий
            pm_low = calculate_pm("semi-detached", 55, get_eaf(factors))
            factors[factor] = 0.82  # Очень высокий
            pm_high = calculate_pm("semi-detached", 55, get_eaf(factors))
            pm_values.append(pm_high - pm_low)
            tdev_values.append(calculate_tdev("semi-detached", pm_high) - calculate_tdev("semi-detached", pm_low))
            factors[factor] = original

        plot = create_factor_analysis_plot(plot_frame, factors_analysis, pm_values, tdev_values)
        plot.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = COCOMOApp(root)
    root.mainloop()