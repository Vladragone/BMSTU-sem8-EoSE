import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class COCOMOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COCOMO Calculator")
        self.root.geometry("1400x900")

        # Коэффициенты для разных типов проектов
        self.model_params = {
            'organic': {'a': 3.2, 'b': 1.05, 'c': 2.5, 'd': 0.38},
            'semi-detached': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35},
            'embedded': {'a': 2.8, 'b': 1.20, 'c': 2.5, 'd': 0.32}
        }

        # Создаем контейнеры
        self.input_frame = ttk.Frame(self.root, padding="15", relief="ridge", width=450)
        self.graph_frame = ttk.Frame(self.root, padding="10")
        self.result_frame = ttk.Frame(self.root, padding="10", relief="ridge")

        self.input_frame.pack(side="left", fill="both", expand=False)
        self.graph_frame.pack(side="top", fill="both", expand=True)
        self.result_frame.pack(side="top", fill="both", expand=False)

        self.input_frame.pack_propagate(False)
        self.input_frame.config(width=450)

        self.create_input_zone()
        self.create_result_zone()

        # Установка значений по умолчанию
        self.size_var.set("55")
        self.model_type.set("semi-detached")
        self.set_default_drivers()

    def create_input_zone(self):
        """Создаем зону ввода данных"""
        ttk.Label(self.input_frame, text="Параметры проекта",
                  font=('Arial', 14, 'bold')).pack(pady=10, anchor="w")

        # Размер проекта
        size_frame = ttk.Frame(self.input_frame)
        size_frame.pack(fill="x", pady=5)
        ttk.Label(size_frame, text="Размер проекта (KLOC):", width=25).pack(side="left")
        self.size_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.size_var, width=15).pack(side="right")

        # Тип проекта
        type_frame = ttk.Frame(self.input_frame)
        type_frame.pack(fill="x", pady=5)
        ttk.Label(type_frame, text="Тип проекта:", width=25).pack(side="left")
        self.model_type = tk.StringVar()
        self.type_combo = ttk.Combobox(type_frame, textvariable=self.model_type,
                                       values=["organic", "semi-detached", "embedded"],
                                       width=25)
        self.type_combo.pack(side="right")

        # Русские названия типов проектов
        self.type_labels = {
            'organic': 'органический',
            'semi-detached': 'промежуточный',
            'embedded': 'встроенный'
        }
        ttk.Label(self.input_frame, textvariable=self.get_type_label_var(),
                  font=('Arial', 10)).pack(anchor="w")

        # Драйверы затрат
        ttk.Label(self.input_frame, text="Драйверы затрат:",
                  font=('Arial', 12, 'bold')).pack(pady=10, anchor="w")

        self.drivers = {}
        self.driver_comboboxes = {}

        driver_info = [
            ('RELY', 'Требуемая надежность', [0.75, 0.86, 1.0, 1.15, 1.4],
             ["Очень низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"]),
            ('DATA', 'Размер базы данных', [0.94, 0.94, 1.0, 1.08, 1.16],
             ["Низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"]),
            ('CPLX', 'Сложность продукта', [0.7, 0.85, 1.0, 1.15, 1.3],
             ["Очень низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"]),
            ('TIME', 'Ограничения по времени', [1.0, 1.11],
             ["Номинальный", "Высокий"]),
            ('ACAP', 'Способности аналитика', [1.46, 1.19, 1.0, 0.86, 0.71],
             ["Очень низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"]),
            ('PCAP', 'Способности программиста', [1.42, 1.17, 1.0, 0.86, 0.7],
             ["Очень низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"]),
            ('MODP', 'Современные методы', [1.24, 1.1, 1.0, 0.91, 0.82],
             ["Очень низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"]),
            ('TOOL', 'Инструменты разработки', [1.24, 1.1, 1.0, 0.91, 0.82],
             ["Очень низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"])
        ]

        for code, name, values, labels in driver_info:
            frame = ttk.Frame(self.input_frame)
            frame.pack(fill="x", pady=3)

            ttk.Label(frame, text=f"{name} ({code}):", width=30, anchor="w").pack(side="left")

            self.drivers[code] = tk.StringVar()
            cb = ttk.Combobox(frame, textvariable=self.drivers[code],
                              values=[f"{label} ({value})" for label, value in zip(labels, values)],
                              state="readonly", width=30)
            cb.pack(side="right", padx=5)
            self.driver_comboboxes[code] = cb

        # Кнопка расчета
        ttk.Button(self.input_frame, text="РАССЧИТАТЬ ПРОЕКТ",
                   command=self.calculate, style='Large.TButton').pack(pady=20)

        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 12), padding=6)

    def get_type_label_var(self):
        """Возвращает текст с русским названием типа проекта"""
        self.type_label_var = tk.StringVar()
        self.model_type.trace_add('write', self.update_type_label)
        self.update_type_label()
        return self.type_label_var

    def update_type_label(self, *args):
        """Обновляет русское название типа проекта"""
        current_type = self.model_type.get()
        self.type_label_var.set(f"Тип: {self.type_labels.get(current_type, '')}")

    def set_default_drivers(self):
        """Установка значений драйверов по умолчанию"""
        default_values = {
            'RELY': "Номинальный (1.0)",
            'DATA': "Высокий (1.08)",
            'CPLX': "Номинальный (1.0)",
            'TIME': "Номинальный (1.0)",
            'ACAP': "Высокий (0.86)",
            'PCAP': "Номинальный (1.0)",
            'MODP': "Номинальный (1.0)",
            'TOOL': "Номинальный (1.0)"
        }

        for code, value in default_values.items():
            self.drivers[code].set(value)

    def create_result_zone(self):
        """Создаем зону вывода результатов"""
        ttk.Label(self.result_frame, text="Результаты расчета",
                  font=('Arial', 12, 'bold')).pack()

        self.pm_label = ttk.Label(self.result_frame, text="Трудоемкость (PM): ")
        self.pm_label.pack(anchor="w")

        self.tm_label = ttk.Label(self.result_frame, text="Время разработки (TM): ")
        self.tm_label.pack(anchor="w")

        # Холст для графиков распределения
        self.dist_canvas_frame = ttk.Frame(self.result_frame)
        self.dist_canvas_frame.pack(fill="both", expand=True)

    def get_driver_value(self, driver_str):
        """Извлекает числовое значение из строки драйвера"""
        try:
            return float(driver_str.split("(")[1].rstrip(")"))
        except:
            return 1.0  # Значение по умолчанию при ошибке

    def calculate(self):
        try:
            size = float(self.size_var.get())
            model_type = self.model_type.get()

            if model_type not in self.model_params:
                raise ValueError("Неверный тип проекта")

            # Получаем значения драйверов
            drivers = {code: self.get_driver_value(var.get())
                       for code, var in self.drivers.items()}

            # Расчет основных показателей
            eaf = self.calculate_eaf(drivers)
            params = self.model_params[model_type]
            pm = params['a'] * eaf * (size ** params['b'])
            tm = params['c'] * (pm ** params['d'])

            # Обновление результатов
            self.pm_label.config(text=f"Трудоемкость (PM): {pm:.1f} чел.-мес.")
            self.tm_label.config(text=f"Время разработки (TM): {tm:.1f} мес.")

            # Построение графиков
            self.plot_combined_impact(size, drivers, model_type)
            self.plot_distribution(pm, tm)
            self.plot_staffing(pm, tm)

        except ValueError as e:
            tk.messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    def calculate_eaf(self, drivers):
        eaf = 1.0
        for factor in drivers.values():
            eaf *= factor
        return eaf

    def plot_combined_impact(self, size, base_drivers, model_type):
        """Графики влияния драйверов на PM и TM"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        ax1, ax2, ax3, ax4 = axes.flatten()

        drivers_to_analyze = ['ACAP', 'PCAP', 'MODP', 'TOOL']
        level_names = ['Оч. низк', 'Низк', 'Ном', 'Высок', 'Оч. выс']

        driver_values = {
            'ACAP': [1.46, 1.19, 1.0, 0.86, 0.71],
            'PCAP': [1.42, 1.17, 1.0, 0.86, 0.7],
            'MODP': [1.24, 1.1, 1.0, 0.91, 0.82],
            'TOOL': [1.24, 1.1, 1.0, 0.91, 0.82],
            'TIME': [1.0, 1.11],
            'RELY': [1.0, 1.15]
        }

        params = self.model_params[model_type]

        for driver in drivers_to_analyze:
            pm_values = []

            for val in driver_values[driver]:
                temp_drivers = base_drivers.copy()
                temp_drivers[driver] = val
                eaf = self.calculate_eaf(temp_drivers)
                pm = params['a'] * eaf * (size ** params['b'])
                pm_values.append(pm)

            ax1.plot(level_names, pm_values, marker='o', label=driver)

        ax1.set_title(f'Влияние драйверов на трудоемкость (PM)\nТип проекта: {self.type_labels[model_type]}')
        ax1.set_xlabel('Уровень драйвера')
        ax1.set_ylabel('Человеко-месяцы')
        ax1.legend()
        ax1.grid(True)

        for driver in drivers_to_analyze:
            tm_values = []

            for val in driver_values[driver]:
                temp_drivers = base_drivers.copy()
                temp_drivers[driver] = val
                eaf = self.calculate_eaf(temp_drivers)
                pm = params['a'] * eaf * (size ** params['b'])
                tm = params['c'] * (pm ** params['d'])
                tm_values.append(tm)

            ax2.plot(level_names, tm_values, marker='o', label=driver)

        ax2.set_title(f'Влияние драйверов на время разработки (TM)\nТип проекта: {self.type_labels[model_type]}')
        ax2.set_xlabel('Уровень драйвера')
        ax2.set_ylabel('Месяцы')
        ax2.legend()
        ax2.grid(True)

        scenario_level_names = {
            'TIME': ['Номинальный', 'Высокий'],
            'RELY': ['Номинальный', 'Высокий']
        }

        def get_fixed_high_scenario_values(varied_driver):
            pm_values = []
            tm_values = []

            for val in driver_values[varied_driver]:
                temp_drivers = base_drivers.copy()
                temp_drivers['MODP'] = 0.82
                temp_drivers['TOOL'] = 0.82
                temp_drivers[varied_driver] = val
                eaf = self.calculate_eaf(temp_drivers)
                pm = params['a'] * eaf * (size ** params['b'])
                tm = params['c'] * (pm ** params['d'])
                pm_values.append(pm)
                tm_values.append(tm)

            return pm_values, tm_values

        rely_pm_values, rely_tm_values = get_fixed_high_scenario_values('RELY')
        time_pm_values, time_tm_values = get_fixed_high_scenario_values('TIME')

        ax3.plot(scenario_level_names['RELY'], rely_pm_values, marker='o', label='RELY')
        ax3.plot(scenario_level_names['TIME'], time_pm_values, marker='s', label='TIME')
        ax3.set_title('MODP и TOOL = высокие\nВлияние RELY и TIME на трудоемкость (PM)')
        ax3.set_xlabel('Уровень драйвера')
        ax3.set_ylabel('Человеко-месяцы')
        ax3.legend()
        ax3.grid(True)

        ax4.plot(scenario_level_names['RELY'], rely_tm_values, marker='o', label='RELY')
        ax4.plot(scenario_level_names['TIME'], time_tm_values, marker='s', label='TIME')
        ax4.set_title('MODP и TOOL = высокие\nВлияние RELY и TIME на время разработки (TM)')
        ax4.set_xlabel('Уровень драйвера')
        ax4.set_ylabel('Месяцы')
        ax4.legend()
        ax4.grid(True)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_distribution(self, pm, tm):
        """Графики распределения работ и времени"""
        for widget in self.dist_canvas_frame.winfo_children():
            widget.destroy()

        # Устанавливаем размеры шрифтов
        plt.rcParams.update({
            'font.size': 8,
            'axes.titlesize': 10,
            'axes.labelsize': 8
        })

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

        # 1. Распределение трудозатрат по этапам
        effort_dist = {
            'Планирование': pm * 0.08,
            'Проектирование': pm * 0.18,
            'Дет. проектирование': pm * 0.25,
            'Кодирование': pm * 0.26,
            'Интеграция': pm * 0.31
        }
        wedges1, texts1, autotexts1 = ax1.pie(
            effort_dist.values(), labels=effort_dist.keys(),
            autopct='%1.1f%%', textprops={'fontsize': 7})
        ax1.set_title('Трудозатраты по этапам (чел.-мес.)')

        # Уменьшаем наложение подписей
        plt.setp(autotexts1, size=7)
        plt.setp(texts1, size=7)

        # 2. Распределение времени по этапам
        time_dist = {
            'Планирование': tm * 0.36,
            'Проектирование': tm * 0.36,
            'Дет. проектирование': tm * 0.18,
            'Кодирование': tm * 0.18,
            'Интеграция': tm * 0.28
        }
        wedges2, texts2, autotexts2 = ax2.pie(
            time_dist.values(), labels=time_dist.keys(),
            autopct='%1.1f%%', textprops={'fontsize': 7})
        ax2.set_title('Время по этапам (мес.)')

        plt.setp(autotexts2, size=7)
        plt.setp(texts2, size=7)

        # 3. Распределение бюджета по видам деятельности
        budget_dist = {
            'Анализ': 0.04,
            'Проектирование': 0.12,
            'Программирование': 0.44,
            'Тестирование': 0.06,
            'Верификация': 0.14,
            'Канцелярия': 0.07,
            'Упр. конфиг.': 0.07,
            'Руководства': 0.06,
        }
        wedges3, texts3, autotexts3 = ax3.pie(
            budget_dist.values(), labels=budget_dist.keys(),
            autopct='%1.1f%%', textprops={'fontsize': 7})
        ax3.set_title('Распределение бюджета')

        plt.setp(autotexts3, size=7)
        plt.setp(texts3, size=7)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.dist_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_staffing(self, pm, tm):
        """Диаграмма привлечения сотрудников в отдельном окне"""
        # Создаем новое окно
        staffing_window = tk.Toplevel(self.root)
        staffing_window.title("Диаграмма привлечения сотрудников")
        staffing_window.geometry("800x500")

        # Рассчитываем количество сотрудников для каждого этапа
        staffing_data = {
            'Планирование': (pm * 0.08) / (tm * 0.36),
            'Проектирование': (pm * 0.18) / (tm * 0.36),
            'Дет. проектирование': (pm * 0.25) / (tm * 0.18),
            'Кодирование': (pm * 0.26) / (tm * 0.18),
            'Интеграция': (pm * 0.31) / (tm * 0.28)
        }

        # Нормализуем данные относительно максимума (100%)
        max_staff = max(staffing_data.values())
        normalized_staff = {k: (v / max_staff) * 100 for k, v in staffing_data.items()}

        # Создаем график
        fig, ax = plt.subplots(figsize=(10, 5))

        # Цвета для каждого этапа
        colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974']

        # Строим столбчатую диаграмму
        bars = ax.bar(normalized_staff.keys(), normalized_staff.values(), color=colors)

        # Настройки графика
        ax.set_title('Диаграмма привлечения сотрудников', fontsize=12)
        ax.set_xlabel('Этапы проекта', fontsize=10)
        ax.set_ylabel('Количество сотрудников (% от максимума)', fontsize=10)
        ax.set_ylim(0, 110)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Добавляем точные значения над столбцами
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=9)

        # Добавляем подпись с фактическим максимальным количеством сотрудников
        ax.text(0.02, 0.95,
                f'Максимальное количество: {max_staff:.1f} ставок.',
                transform=ax.transAxes, fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8))

        plt.tight_layout()

        # Отображаем график в новом окне
        canvas = FigureCanvasTkAgg(fig, master=staffing_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = COCOMOApp(root)
    root.mainloop()
