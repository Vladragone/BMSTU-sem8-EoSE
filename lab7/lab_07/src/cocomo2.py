"""
COCOMO 2 — Лабораторная работа №7, Вариант 2 (Биржа)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

# ── ТАБЛИЦЫ ДАННЫХ ────────────────────────────────────────────

# Таблица весов функциональных точек
FP_WEIGHTS = {
    'EI':  [3, 4, 6],
    'EO':  [4, 5, 7],
    'EQ':  [3, 4, 6],
    'ILF': [7, 10, 15],
    'EIF': [5, 7, 10],
}

# Строк кода на функциональную точку по языку
LANG_SLOC = {
    'ASM':    320,
    'C':      128,
    'Cobol':  106,
    'Fortran':106,
    'Pascal':  90,
    'C++':     53,
    'Java':    53,
    'C#':      53,
    'Ada 95':  49,
    'SQL':    125,
    'Visual C++': 34,
    'Delphi':  29,
    'Perl':    21,
    'Prolog':  54,
}

# Факторы показателя степени (scale drivers)
SCALE_PARAMS = {
    'PREC': [6.20, 4.96, 3.72, 2.48, 1.24, 0.00],
    'FLEX': [5.07, 4.05, 3.04, 2.03, 1.01, 0.00],
    'RESL': [7.07, 5.65, 4.24, 2.83, 1.41, 0.00],
    'TEAM': [5.48, 4.38, 3.29, 2.19, 1.10, 0.00],
    'PMAT': [7.80, 6.24, 4.68, 3.12, 1.56, 0.00],
}

SCALE_LABELS = {
    'PREC': ('Новизна проекта', [
        'Полное отсутствие прецедентов',
        'Почти полное отсутствие прецедентов',
        'Наличие некоторых прецедентов',
        'Общее знакомство с проектом',
        'Значительное знакомство с проектом',
        'Полное знакомство с проектом',
    ]),
    'FLEX': ('Гибкость процесса разработки', [
        'Точный, строгий процесс',
        'Случайные послабления в процессе',
        'Некоторые послабления в процессе',
        'Большей частью согласованный процесс',
        'Некоторое согласование процесса',
        'Заказчик определил только общие цели',
    ]),
    'RESL': ('Анализ архитектуры и рисков', [
        'Малое (20%)',
        'Некоторое (40%)',
        'Частое (60%)',
        'В целом (75%)',
        'Почти полное (90%)',
        'Полное (100%)',
    ]),
    'TEAM': ('Сплочённость команды', [
        'Сильно затруднённое взаимодействие',
        'Несколько затруднённое взаимодействие',
        'Некоторая согласованность',
        'Повышенная согласованность',
        'Высокая согласованность',
        'Взаимодействие как в едином целом',
    ]),
    'PMAT': ('Уровень развития процесса', [
        'Уровень 1 СММ',
        'Уровень 1+ СММ',
        'Уровень 2 СММ',
        'Уровень 3 СММ',
        'Уровень 4 СММ',
        'Уровень 5 СММ',
    ]),
}

# Факторы трудоёмкости (early design)
LABOR_FACTORS = {
    'PERS': {
        'name': 'Возможности персонала (PERS)',
        'levels': ['Очень низкий', 'Низкий', 'Номинальный', 'Высокий', 'Очень высокий', 'Сверхвысокий'],
        'values': [1.62, 1.26, 1.00, 0.83, 0.63, 0.50],
    },
    'RCPX': {
        'name': 'Надёжность и сложность (RCPX)',
        'levels': ['Очень низкий', 'Низкий', 'Номинальный', 'Высокий', 'Очень высокий', 'Сверхвысокий'],
        'values': [0.60, 0.83, 1.00, 1.33, 1.91, 2.72],
    },
    'RUSE': {
        'name': 'Повторное использование (RUSE)',
        'levels': ['Низкий', 'Номинальный', 'Высокий', 'Очень высокий', 'Сверхвысокий'],
        'values': [0.95, 1.00, 1.07, 1.15, 1.24],
    },
    'PDIF': {
        'name': 'Сложность платформы (PDIF)',
        'levels': ['Низкий', 'Номинальный', 'Высокий', 'Очень высокий', 'Сверхвысокий'],
        'values': [0.87, 1.00, 1.29, 1.81, 2.61],
    },
    'PREX': {
        'name': 'Опыт персонала (PREX)',
        'levels': ['Очень низкий', 'Низкий', 'Номинальный', 'Высокий', 'Очень высокий', 'Сверхвысокий'],
        'values': [1.33, 1.22, 1.00, 0.87, 0.74, 0.62],
    },
    'FCIL': {
        'name': 'Инструментальные средства (FCIL)',
        'levels': ['Очень низкий', 'Низкий', 'Номинальный', 'Высокий', 'Очень высокий', 'Сверхвысокий'],
        'values': [1.30, 1.10, 1.00, 0.87, 0.73, 0.62],
    },
    'SCED': {
        'name': 'Требуемые сроки (SCED)',
        'levels': ['Очень низкий', 'Низкий', 'Номинальный', 'Высокий', 'Очень высокий'],
        'values': [1.43, 1.14, 1.00, 1.00, 1.00],
    },
}

# Весовые коэффициенты для модели композиции
COMP_SCREEN_WEIGHTS = [1, 2, 3]   # simple, medium, hard
COMP_REPORT_WEIGHTS = [2, 5, 8]   # simple, medium, hard
COMP_GEN3_WEIGHT    = 10
COMP_EXP_RATES      = [4, 7, 13, 25, 50]  # NOP/месяц по уровням опытности

# ── ЦВЕТА И ШРИФТЫ ────────────────────────────────────────────

C_BG      = '#FFFFFF'
C_BG2     = '#F0F4FA'
C_BG3     = '#DCE8F5'
C_ACCENT  = '#0D3B8C'
C_ACCENT2 = '#1565C0'
C_ACCENT3 = '#64B5F6'
C_FG      = '#1A1A1A'
C_FG2     = '#37474F'
C_BORDER  = '#BBCDE5'
C_ROW_ALT = '#EBF2FB'
C_RES_BG  = '#E8F5E9'
C_RES_FG  = '#1B5E20'

F_HUGE   = ('Segoe UI', 18, 'bold')
F_TITLE  = ('Segoe UI', 14, 'bold')
F_LABEL  = ('Segoe UI', 13)
F_BOLD   = ('Segoe UI', 13, 'bold')
F_COMBO  = ('Segoe UI', 12)
F_TABLE  = ('Segoe UI', 12)
F_TABLEB = ('Segoe UI', 12, 'bold')
F_SMALL  = ('Segoe UI', 11)
F_RESULT = ('Consolas', 13, 'bold')
F_BTN    = ('Segoe UI', 13, 'bold')

# ── СТИЛИ TTK ─────────────────────────────────────────────────

def apply_styles(root):
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('TFrame',      background=C_BG)
    s.configure('Card.TFrame', background=C_BG2)
    s.configure('TLabel',      background=C_BG,  foreground=C_FG,     font=F_LABEL)
    s.configure('Card.TLabel', background=C_BG2, foreground=C_FG,     font=F_LABEL)
    s.configure('Head.TLabel', background=C_BG2, foreground=C_ACCENT, font=F_TITLE)
    s.configure('TNotebook',      background=C_BG3, tabmargins=[2, 4, 2, 0])
    s.configure('TNotebook.Tab',  background=C_BG3, foreground=C_FG2,
                padding=[16, 8], font=F_BOLD)
    s.map('TNotebook.Tab',
          background=[('selected', C_ACCENT2)],
          foreground=[('selected', '#FFFFFF')])
    s.configure('TCombobox', fieldbackground=C_BG, background=C_BG, foreground=C_FG,
                font=F_COMBO, arrowcolor=C_ACCENT2, relief='flat',
                bordercolor=C_BORDER, lightcolor=C_BORDER, darkcolor=C_BORDER)
    s.map('TCombobox',
          fieldbackground=[('readonly', C_BG)],
          foreground=[('readonly', C_FG)],
          bordercolor=[('focus', C_ACCENT2)])
    s.configure('Treeview', background=C_BG, fieldbackground=C_BG,
                foreground=C_FG, rowheight=30, font=F_TABLE,
                borderwidth=0, relief='flat')
    s.configure('Treeview.Heading', background=C_BG3, foreground=C_ACCENT,
                font=F_TABLEB, relief='flat', bordercolor=C_BORDER)
    s.map('Treeview',
          background=[('selected', C_ACCENT2)],
          foreground=[('selected', '#FFFFFF')])
    s.configure('Group.TLabelframe', background=C_BG2, relief='groove',
                bordercolor=C_BORDER, borderwidth=2)
    s.configure('Group.TLabelframe.Label', background=C_BG2, foreground=C_ACCENT, font=F_BOLD)
    s.configure('TSeparator', background=C_BORDER)
    s.configure('TSpinbox', fieldbackground=C_BG, background=C_BG2,
                foreground=C_FG, font=F_LABEL, arrowcolor=C_ACCENT2,
                bordercolor=C_BORDER, lightcolor=C_BORDER, darkcolor=C_BORDER)
    s.map('TSpinbox', fieldbackground=[('focus', '#EAF0FB')],
          bordercolor=[('focus', C_ACCENT2)])
    s.configure('TEntry', fieldbackground=C_BG, foreground=C_FG, font=F_LABEL,
                bordercolor=C_BORDER, lightcolor=C_BORDER, darkcolor=C_BORDER)
    s.map('TEntry', fieldbackground=[('focus', '#EAF0FB')],
          bordercolor=[('focus', C_ACCENT2)])


def make_btn(parent, text, command, width=22):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=C_ACCENT2, fg='#FFFFFF',
        font=F_BTN, relief='flat', cursor='hand2',
        activebackground='#0D3B8C', activeforeground='#FFFFFF',
        padx=18, pady=10, width=width,
    )
    btn.bind('<Enter>', lambda e: btn.config(bg='#0D3B8C'))
    btn.bind('<Leave>', lambda e: btn.config(bg=C_ACCENT2))
    return btn


def result_label(parent, textvariable=None, text=''):
    kw = dict(bg=C_RES_BG, fg=C_RES_FG, font=F_RESULT,
              relief='flat', padx=12, pady=8, anchor='w',
              justify='left')
    if textvariable:
        return tk.Label(parent, textvariable=textvariable, **kw)
    return tk.Label(parent, text=text, **kw)


def lf(parent, text):
    return ttk.LabelFrame(parent, text=text, style='Group.TLabelframe', padding=10)


def separator(parent):
    ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=8)


# ── ГЛАВНОЕ ПРИЛОЖЕНИЕ ────────────────────────────────────────

class COCOMO2App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('COCOMO 2 — Вариант 2: Биржа')
        self.geometry('1050x800')
        self.minsize(900, 700)
        self.configure(bg=C_BG)
        apply_styles(self)

        # Заголовок
        hdr = tk.Frame(self, bg=C_ACCENT, pady=14)
        hdr.pack(fill='x')
        tk.Label(hdr, text='COCOMO 2  ·  Оценка стоимости ПО', bg=C_ACCENT,
                 fg='#FFFFFF', font=F_HUGE).pack()
        tk.Label(hdr, text='Вариант 2 — Мобильное приложение брокерской системы',
                 bg=C_ACCENT, fg=C_ACCENT3, font=F_LABEL).pack()

        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=12, pady=12)

        # Вкладки
        self.tab_fp   = ttk.Frame(nb, style='TFrame')
        self.tab_pow  = ttk.Frame(nb, style='TFrame')
        self.tab_arch = ttk.Frame(nb, style='TFrame')
        self.tab_comp = ttk.Frame(nb, style='TFrame')

        nb.add(self.tab_fp,   text='  Функциональные точки  ')
        nb.add(self.tab_pow,  text='  Показатель степени  ')
        nb.add(self.tab_arch, text='  Ранняя архитектура  ')
        nb.add(self.tab_comp, text='  Модель композиции  ')

        # Общие данные (LOC, P)
        self.LOC = 0
        self.P   = 1.01

        self._build_fp_tab()
        self._build_pow_tab()
        self._build_arch_tab()
        self._build_comp_tab()

        # Установить значения варианта 2
        self._preset_variant2()

    # ── ВКЛАДКА 1: ФУНКЦИОНАЛЬНЫЕ ТОЧКИ ──────────────────────

    def _build_fp_tab(self):
        tab = self.tab_fp
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(1, weight=1)

        # --- Левая колонка: характеристики продукта ---
        left = lf(tab, 'Характеристики продукта (14 факторов, 0–5)')
        left.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(10,5), pady=10)

        self.sys_params = []
        param_names = [
            'Обмен данными',
            'Распределённая обработка',
            'Производительность',
            'Эксплуатационные ограничения\nпо аппаратным ресурсам',
            'Транзакционная нагрузка',
            'Оперативный ввод данных',
            'Эргономические характеристики\n(работа конечных пользователей)',
            'Оперативное обновление',
            'Сложность обработки',
            'Повторное использование',
            'Лёгкость инсталляции',
            'Лёгкость эксплуатации',
            'Портируемость',
            'Гибкость',
        ]
        for i, name in enumerate(param_names):
            ttk.Label(left, text=name, style='Card.TLabel').grid(
                row=i, column=0, sticky='w', pady=2, padx=4)
            var = tk.IntVar(value=0)
            sp = ttk.Spinbox(left, from_=0, to=5, width=5,
                             textvariable=var, font=F_LABEL)
            sp.grid(row=i, column=1, sticky='e', pady=2, padx=4)
            self.sys_params.append(var)

        # --- Правая верхняя: функциональные точки ---
        right_top = lf(tab, 'Функциональные точки (FP)')
        right_top.grid(row=0, column=1, sticky='nsew', padx=(5,10), pady=(10,5))
        right_top.columnconfigure(1, weight=1)
        right_top.columnconfigure(2, weight=2)
        right_top.columnconfigure(3, weight=1)

        headers = ['Тип', 'Кол-во', 'Сложность', 'Итого']
        for c, h in enumerate(headers):
            ttk.Label(right_top, text=h, style='Card.TLabel',
                      font=F_BOLD).grid(row=0, column=c, padx=6, pady=4, sticky='w')

        fp_rows = [
            ('EI  (Внешние вводы)',         'EI'),
            ('EO  (Внешние выводы)',         'EO'),
            ('EQ  (Внешние запросы)',        'EQ'),
            ('ILF (Внутр. лог. файлы)',     'ILF'),
            ('EIF (Внешн. интерф. файлы)',  'EIF'),
        ]
        fp_complexity = {
            'EI':  ['Низкий (3)',  'Средний (4)', 'Высокий (6)'],
            'EO':  ['Низкий (4)',  'Средний (5)', 'Высокий (7)'],
            'EQ':  ['Низкий (3)',  'Средний (4)', 'Высокий (6)'],
            'ILF': ['Низкий (7)',  'Средний (10)','Высокий (15)'],
            'EIF': ['Низкий (5)',  'Средний (7)', 'Высокий (10)'],
        }

        self.fp_qty  = {}
        self.fp_dif  = {}
        self.fp_res  = {}

        for r, (label, key) in enumerate(fp_rows, start=1):
            ttk.Label(right_top, text=label, style='Card.TLabel').grid(
                row=r, column=0, sticky='w', padx=6, pady=3)
            var_qty = tk.IntVar(value=1)
            sp = ttk.Spinbox(right_top, from_=0, to=999, width=6,
                             textvariable=var_qty, font=F_LABEL)
            sp.grid(row=r, column=1, padx=6, pady=3, sticky='ew')
            cb = ttk.Combobox(right_top, values=fp_complexity[key],
                              state='readonly', width=16, font=F_COMBO)
            cb.current(0)
            cb.grid(row=r, column=2, padx=6, pady=3, sticky='ew')
            lbl_res = ttk.Label(right_top, text='0', style='Card.TLabel', font=F_BOLD)
            lbl_res.grid(row=r, column=3, padx=6, pady=3, sticky='e')
            self.fp_qty[key] = var_qty
            self.fp_dif[key] = cb
            self.fp_res[key] = lbl_res

        # Итого FP
        ttk.Label(right_top, text='Итого FP (UFPC):', style='Card.TLabel',
                  font=F_BOLD).grid(row=6, column=2, sticky='e', padx=6, pady=6)
        self.ufpc_lbl = ttk.Label(right_top, text='0', style='Card.TLabel', font=F_BOLD)
        self.ufpc_lbl.grid(row=6, column=3, sticky='e', padx=6)

        # --- Правая нижняя: языки программирования ---
        right_bot = lf(tab, 'Процент использования языка программирования')
        right_bot.grid(row=1, column=1, sticky='nsew', padx=(5,10), pady=(5,10))

        langs = list(LANG_SLOC.keys())
        self.lang_pct = {}
        for i, lang in enumerate(langs):
            r, c = divmod(i, 2)
            ttk.Label(right_bot, text=f'{lang}:', style='Card.TLabel').grid(
                row=r, column=c*2, sticky='w', padx=6, pady=2)
            var = tk.DoubleVar(value=0.0)
            e = ttk.Entry(right_bot, textvariable=var, width=8, font=F_LABEL)
            e.grid(row=r, column=c*2+1, sticky='ew', padx=6, pady=2)
            self.lang_pct[lang] = var

        # --- Результаты ---
        res_frame = tk.Frame(tab, bg=C_BG)
        res_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

        self.fp_result_var = tk.StringVar(value='← Нажмите «Рассчитать»')
        rl = result_label(res_frame, textvariable=self.fp_result_var)
        rl.pack(side='left', fill='x', expand=True, padx=(0,10))

        make_btn(res_frame, '⟳  Рассчитать FP', self.calculate_fp, width=20).pack(side='right')

    # ── ВКЛАДКА 2: ПОКАЗАТЕЛЬ СТЕПЕНИ ─────────────────────────

    def _build_pow_tab(self):
        tab = self.tab_pow
        tab.columnconfigure(0, weight=1)

        card = lf(tab, 'Факторы показателя степени модели COCOMO 2')
        card.pack(fill='x', padx=20, pady=20)
        card.columnconfigure(1, weight=1)

        self.scale_vars = {}
        for i, (key, (name, levels)) in enumerate(SCALE_LABELS.items()):
            ttk.Label(card, text=f'{key} — {name}:', style='Card.TLabel',
                      font=F_BOLD).grid(row=i, column=0, sticky='w', padx=8, pady=5)
            cb = ttk.Combobox(card, values=levels, state='readonly',
                              width=52, font=F_COMBO)
            cb.current(0)
            cb.grid(row=i, column=1, sticky='ew', padx=8, pady=5)
            self.scale_vars[key] = cb

        # Результат P
        res = tk.Frame(tab, bg=C_BG)
        res.pack(fill='x', padx=20, pady=10)
        self.pow_result_var = tk.StringVar(value='← Нажмите «Рассчитать»')
        result_label(res, textvariable=self.pow_result_var).pack(side='left', fill='x', expand=True, padx=(0,10))
        make_btn(res, '⟳  Рассчитать P', self.calculate_p, width=18).pack(side='right')

        # Формула
        note = tk.Frame(tab, bg=C_BG2, pady=8)
        note.pack(fill='x', padx=20, pady=10)
        tk.Label(note, text='Формула:  P = 1.01 + 0.01 × Σ(SF_i)',
                 bg=C_BG2, fg=C_ACCENT, font=F_LABEL).pack()
        tk.Label(note, text='Трудозатраты:  PM = 2.45 × EAF × (KLOC ^ P)',
                 bg=C_BG2, fg=C_ACCENT, font=F_LABEL).pack()

    # ── ВКЛАДКА 3: РАННЯЯ АРХИТЕКТУРА ─────────────────────────

    def _build_arch_tab(self):
        tab = self.tab_arch
        tab.columnconfigure(0, weight=1)

        note_fr = tk.Frame(tab, bg='#FFF8E1', pady=6, padx=10)
        note_fr.pack(fill='x', padx=20, pady=(15,0))
        tk.Label(note_fr,
                 text='ℹ  Перед расчётом заполните вкладки «Функциональные точки» и «Показатель степени»',
                 bg='#FFF8E1', fg='#5D4037', font=F_SMALL).pack()

        card = lf(tab, 'Факторы трудоёмкости (Early Design)')
        card.pack(fill='x', padx=20, pady=10)
        card.columnconfigure(1, weight=1)

        self.arch_vars = {}
        for i, (key, info) in enumerate(LABOR_FACTORS.items()):
            ttk.Label(card, text=info['name'] + ':', style='Card.TLabel',
                      font=F_BOLD).grid(row=i, column=0, sticky='w', padx=8, pady=5)
            cb = ttk.Combobox(card, values=info['levels'], state='readonly',
                              width=30, font=F_COMBO)
            cb.current(0)
            cb.grid(row=i, column=1, sticky='ew', padx=8, pady=5)
            self.arch_vars[key] = cb

        sal_fr = lf(tab, 'Финансовые параметры')
        sal_fr.pack(fill='x', padx=20, pady=5)
        ttk.Label(sal_fr, text='Средняя зарплата (руб./мес.):', style='Card.TLabel').grid(
            row=0, column=0, sticky='w', padx=8)
        self.arch_salary = tk.DoubleVar(value=90000)
        ttk.Entry(sal_fr, textvariable=self.arch_salary, width=14, font=F_LABEL).grid(
            row=0, column=1, sticky='w', padx=8)

        res_fr = tk.Frame(tab, bg=C_BG)
        res_fr.pack(fill='x', padx=20, pady=10)
        self.arch_result_var = tk.StringVar(value='← Нажмите «Рассчитать»')
        result_label(res_fr, textvariable=self.arch_result_var).pack(side='left', fill='x', expand=True, padx=(0,10))
        make_btn(res_fr, '⟳  Рассчитать', self.calculate_arch, width=18).pack(side='right')

    # ── ВКЛАДКА 4: МОДЕЛЬ КОМПОЗИЦИИ ──────────────────────────

    def _build_comp_tab(self):
        tab = self.tab_comp
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)

        # Экранные формы
        frm_screens = lf(tab, 'Экранные формы')
        frm_screens.grid(row=0, column=0, sticky='nsew', padx=(20,5), pady=10)

        ttk.Label(frm_screens, text='Сложность', style='Card.TLabel',
                  font=F_BOLD).grid(row=0, column=1, padx=6)
        ttk.Label(frm_screens, text='NOP-вес', style='Card.TLabel',
                  font=F_BOLD).grid(row=0, column=2, padx=6)
        ttk.Label(frm_screens, text='Кол-во', style='Card.TLabel',
                  font=F_BOLD).grid(row=0, column=3, padx=6)

        self.screen_qty = []
        for r, (lvl, w) in enumerate([('Простые', 1), ('Средние', 2), ('Сложные', 3)], 1):
            ttk.Label(frm_screens, text=lvl, style='Card.TLabel').grid(
                row=r, column=1, sticky='w', padx=6, pady=4)
            ttk.Label(frm_screens, text=str(w), style='Card.TLabel').grid(
                row=r, column=2, padx=6)
            var = tk.IntVar(value=0)
            ttk.Spinbox(frm_screens, from_=0, to=999, textvariable=var,
                        width=7, font=F_LABEL).grid(row=r, column=3, padx=6, pady=4)
            self.screen_qty.append(var)

        # Отчёты
        frm_reports = lf(tab, 'Отчёты')
        frm_reports.grid(row=0, column=1, sticky='nsew', padx=(5,20), pady=10)

        ttk.Label(frm_reports, text='Сложность', style='Card.TLabel',
                  font=F_BOLD).grid(row=0, column=1, padx=6)
        ttk.Label(frm_reports, text='NOP-вес', style='Card.TLabel',
                  font=F_BOLD).grid(row=0, column=2, padx=6)
        ttk.Label(frm_reports, text='Кол-во', style='Card.TLabel',
                  font=F_BOLD).grid(row=0, column=3, padx=6)

        self.report_qty = []
        for r, (lvl, w) in enumerate([('Простые', 2), ('Средние', 5), ('Сложные', 8)], 1):
            ttk.Label(frm_reports, text=lvl, style='Card.TLabel').grid(
                row=r, column=1, sticky='w', padx=6, pady=4)
            ttk.Label(frm_reports, text=str(w), style='Card.TLabel').grid(
                row=r, column=2, padx=6)
            var = tk.IntVar(value=0)
            ttk.Spinbox(frm_reports, from_=0, to=999, textvariable=var,
                        width=7, font=F_LABEL).grid(row=r, column=3, padx=6, pady=4)
            self.report_qty.append(var)

        # Доп. параметры
        frm_extra = lf(tab, 'Дополнительные параметры')
        frm_extra.grid(row=1, column=0, columnspan=2, sticky='ew', padx=20, pady=5)
        frm_extra.columnconfigure(1, weight=1)

        ttk.Label(frm_extra, text='Модулей на языках 3-го поколения (вес 10):', style='Card.TLabel').grid(
            row=0, column=0, sticky='w', padx=8, pady=4)
        self.gen3_qty = tk.IntVar(value=0)
        ttk.Spinbox(frm_extra, from_=0, to=999, textvariable=self.gen3_qty,
                    width=7, font=F_LABEL).grid(row=0, column=1, sticky='w', padx=8)

        ttk.Label(frm_extra, text='%RUSE (повторное использование, %):', style='Card.TLabel').grid(
            row=1, column=0, sticky='w', padx=8, pady=4)
        self.ruse_pct = tk.DoubleVar(value=0)
        ttk.Entry(frm_extra, textvariable=self.ruse_pct, width=8, font=F_LABEL).grid(
            row=1, column=1, sticky='w', padx=8)

        ttk.Label(frm_extra, text='Опытность команды:', style='Card.TLabel').grid(
            row=2, column=0, sticky='w', padx=8, pady=4)
        self.exp_cb = ttk.Combobox(frm_extra, state='readonly', font=F_COMBO, width=24,
            values=['Очень низкая (4 NOP/мес)', 'Низкая (7 NOP/мес)',
                    'Номинальная (13 NOP/мес)', 'Высокая (25 NOP/мес)', 'Очень высокая (50 NOP/мес)'])
        self.exp_cb.current(0)
        self.exp_cb.grid(row=2, column=1, sticky='w', padx=8, pady=4)

        ttk.Label(frm_extra, text='Средняя зарплата (руб./мес.):', style='Card.TLabel').grid(
            row=3, column=0, sticky='w', padx=8, pady=4)
        self.comp_salary = tk.DoubleVar(value=90000)
        ttk.Entry(frm_extra, textvariable=self.comp_salary, width=14, font=F_LABEL).grid(
            row=3, column=1, sticky='w', padx=8)

        res_fr = tk.Frame(tab, bg=C_BG)
        res_fr.grid(row=2, column=0, columnspan=2, sticky='ew', padx=20, pady=10)
        self.comp_result_var = tk.StringVar(value='← Нажмите «Рассчитать»')
        result_label(res_fr, textvariable=self.comp_result_var).pack(side='left', fill='x', expand=True, padx=(0,10))
        make_btn(res_fr, '⟳  Рассчитать', self.calculate_comp, width=18).pack(side='right')

    # ── ПРЕДУСТАНОВКА ВАРИАНТА 2 ──────────────────────────────

    def _preset_variant2(self):
        """Вариант 2: Биржа — предустановка значений из задания"""
        # Характеристики продукта
        preset_sys = [5, 5, 3, 2, 3, 4, 1, 4, 4, 0, 1, 2, 2, 2]
        for var, val in zip(self.sys_params, preset_sys):
            var.set(val)

        # Функциональные точки (по описанию приложения: 4 страницы)
        # EI: авторизация(1), добавить бумагу(1), оформить заявку(1), удалить/изменить заявку(2) = 5
        # EO: отображение биржевых сводок(1) = 2
        # EQ: список заявок(1), просмотр биржевых сводок(1) = 1
        # ILF: пользователи(1), бумаги(1), заявки(1), котировки(1) = 4
        # EIF: внешняя биржевая система(1) = 1
        self.fp_qty['EI'].set(5)
        self.fp_qty['EO'].set(2)
        self.fp_qty['EQ'].set(1)
        self.fp_qty['ILF'].set(4)
        self.fp_qty['EIF'].set(1)
        self.fp_dif['EI'].current(0)   # Низкий
        self.fp_dif['EO'].current(0)
        self.fp_dif['EQ'].current(0)
        self.fp_dif['ILF'].current(0)
        self.fp_dif['EIF'].current(0)

        # Языки: SQL 15%, C# 60%, Java 25%
        self.lang_pct['SQL'].set(15.0)
        self.lang_pct['C#'].set(60.0)
        self.lang_pct['Java'].set(25.0)

        # Показатель степени — из задания:
        # PREC: "новая команда, некоторый опыт" → наличие некоторых прецедентов (index 2)
        # FLEX: "заказчик не настаивает на жёстком процессе" → Некоторые послабления (index 2)
        # RESL: "лишь некоторое внимание к рискам" → Наличие некоторых прецедентов (index 1)
        # TEAM: "приемлемая коммуникация" → Некоторая согласованность (index 2)
        # PMAT: "только начинает внедрять методы" → Уровень 1 СММ (index 0)
        self.scale_vars['PREC'].current(2)
        self.scale_vars['FLEX'].current(3)
        self.scale_vars['RESL'].current(1)
        self.scale_vars['TEAM'].current(2)
        self.scale_vars['PMAT'].current(1)

        # Факторы трудоёмкости — из задания:
        # PERS: средние → Номинальный (index 2)
        # RCPX: очень высокий (index 4)
        # RUSE: не предусматривается → Низкий (index 0)
        # PDIF: высокий (index 2 в [Низ,Ном,Выс,Оч.выс,Сверх])
        # PREX: низкий → index 1
        # FCIL: очень интенсивное использование → Очень высокий (index 4)
        # SCED: жёсткий график → Очень низкий (index 0)
        self.arch_vars['PERS'].current(2)
        self.arch_vars['RCPX'].current(4)
        self.arch_vars['RUSE'].current(0)
        self.arch_vars['PDIF'].current(2)
        self.arch_vars['PREX'].current(1)
        self.arch_vars['FCIL'].current(4)
        self.arch_vars['SCED'].current(0)

        # Модель композиции — по описанию страниц:
        # Экранные формы: авторизация(1 простая), биржевые сводки(1 средняя),
        #                 заявки(1 средняя), новая заявка(1 простая) + диалог(1 простая)
        self.screen_qty[0].set(1)   # простые
        self.screen_qty[1].set(4)   # средние
        self.screen_qty[2].set(1)   # сложные

        # Отчёты: биржевые сводки и список заявок можно считать
        # представленными отчётами умеренной сложности
        self.report_qty[0].set(0)
        self.report_qty[1].set(2)
        self.report_qty[2].set(0)

        self.gen3_qty.set(2)
        self.ruse_pct.set(0)
        self.exp_cb.current(1)  # Низкая опытность

    # ── РАСЧЁТЫ ───────────────────────────────────────────────

    def calculate_fp(self):
        try:
            qty     = {k: self.fp_qty[k].get()  for k in FP_WEIGHTS}
            dif_idx = {k: self.fp_dif[k].current() for k in FP_WEIGHTS}
            sys_sum = sum(v.get() for v in self.sys_params)

            totals = {}
            ufpc = 0
            for key in FP_WEIGHTS:
                w = FP_WEIGHTS[key][dif_idx[key]]
                t = qty[key] * w
                totals[key] = t
                ufpc += t
                self.fp_res[key].config(text=str(t))

            self.ufpc_lbl.config(text=str(ufpc))

            # Нормировочный коэффициент
            coeff = 0.65 + 0.01 * sys_sum
            afpc  = round(ufpc * coeff, 2)

            # FP = AFPC (нормированное количество)
            fp = afpc

            # Строки кода
            total_pct = sum(self.lang_pct[l].get() for l in LANG_SLOC)
            if abs(total_pct - 100) > 0.5 and total_pct > 0:
                messagebox.showwarning(
                    'Предупреждение',
                    f'Сумма процентов языков = {total_pct:.1f}% (ожидается 100%).\n'
                    'Расчёт выполнен, но результат может быть неточным.')

            loc = 0
            for lang, sloc_per_fp in LANG_SLOC.items():
                pct = self.lang_pct[lang].get()
                loc += fp * (pct / 100.0) * sloc_per_fp
            loc = int(loc)

            self.LOC = loc

            self.fp_result_var.set(
                f'Коэффициент CAF = {coeff:.2f}    '
                f'UFPC = {ufpc}    '
                f'AFPC = {afpc:.2f}\n'
                f'FP = {fp:.2f}    '
                f'SLOC = {loc:,} строк кода'
            )
        except Exception as ex:
            messagebox.showerror('Ошибка', str(ex))

    def calculate_p(self):
        try:
            sf_sum = 0.0
            for key in SCALE_PARAMS:
                idx = self.scale_vars[key].current()
                sf_sum += SCALE_PARAMS[key][idx]
            self.P = 1.01 + 0.01 * sf_sum
            self.pow_result_var.set(
                f'Сумма SF = {sf_sum:.2f}\n'
                f'Показатель степени  P = {self.P:.4f}'
            )
        except Exception as ex:
            messagebox.showerror('Ошибка', str(ex))

    def calculate_arch(self):
        try:
            # Пересчитать FP и P автоматически
            self.calculate_fp()
            self.calculate_p()

            if self.LOC == 0:
                messagebox.showwarning('Предупреждение',
                    'SLOC = 0. Заполните вкладку «Функциональные точки».')
                return

            eaf = 1.0
            for i, (key, info) in enumerate(LABOR_FACTORS.items()):
                idx = self.arch_vars[key].current()
                eaf *= info['values'][idx]

            kloc   = self.LOC / 1000.0
            salary = self.arch_salary.get()

            pm     = round(2.45 * eaf * (kloc ** self.P), 2)
            tm     = round(3.0  * (pm ** (0.33 + 0.2 * (self.P - 1.01))), 2)
            budget = round(salary * pm, 2)

            self.arch_result_var.set(
                f'EAF = {eaf:.4f}    KLOC = {kloc:.3f}    P = {self.P:.4f}\n'
                f'Трудозатраты PM = {pm:.2f} чел./мес.    '
                f'Время TM = {tm:.2f} мес.    '
                f'Бюджет = {budget:,.2f} руб.'
            )
        except Exception as ex:
            messagebox.showerror('Ошибка', str(ex))

    def calculate_comp(self):
        try:
            # Пересчитать показатель степени P
            self.calculate_p()

            screens = [v.get() for v in self.screen_qty]
            reports = [v.get() for v in self.report_qty]
            gen3    = self.gen3_qty.get()
            ruse    = self.ruse_pct.get()
            exp_idx = self.exp_cb.current()
            salary  = self.comp_salary.get()

            nop = (sum(s * w for s, w in zip(screens, COMP_SCREEN_WEIGHTS)) +
                   sum(r * w for r, w in zip(reports, COMP_REPORT_WEIGHTS)) +
                   gen3 * COMP_GEN3_WEIGHT)

            rate   = COMP_EXP_RATES[exp_idx]
            pm     = round(nop * (100 - ruse) / 100.0 / rate, 2)
            tm     = round(3.0 * (pm ** (0.33 + 0.2 * (self.P - 1.01))), 2)
            budget = round(salary * pm, 2)

            self.comp_result_var.set(
                f'NOP = {nop:.1f}    Опытность = {rate} NOP/мес    %%RUSE = {ruse:.1f}%%\n'
                f'Трудозатраты PM = {pm:.2f} чел./мес.    '
                f'Время TM = {tm:.2f} мес.    '
                f'Бюджет = {budget:,.2f} руб.'
            )
        except Exception as ex:
            messagebox.showerror('Ошибка', str(ex))


# ── ЗАПУСК ────────────────────────────────────────────────────

if __name__ == '__main__':
    app = COCOMO2App()
    app.mainloop()
