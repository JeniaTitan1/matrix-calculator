import tkinter as tk
import numpy as np
from tkinter import Tk, Button, Frame, Toplevel, Label, Entry, StringVar, BOTH, messagebox
from tkinter import font as tkfont


class MatrixOperation:
    def __init__(self, operation_name, main_menu, single_matrix=False):
        # Ініціалізація базового класу для операцій з матрицями
        self.gui_input = None  # Для збереження вікна вводу
        self.gui_output = None  # Для збереження вікна виводу
        self.matrix_a = []  # Матриця A
        self.matrix_b = []  # Матриця B
        self.result_matrix = []  # Результуюча матриця
        self.rows, self.cols = None, None  # Кількість рядків та стовпців
        self.operation_name = operation_name  # Назва операції (наприклад, "Додавання")
        self.main_menu = main_menu  # Головне меню для взаємодії з іншими екранними елементами
        self.single_matrix = single_matrix  # Для визначення, чи потрібно працювати з однією матрицею (наприклад,
        # транспонування)
        self.entry_widgets_a = []  # Список віджетів для введення значень матриці A
        self.entry_widgets_b = []  # Список віджетів для введення значень матриці B
        self.create_main_menu()  # Створення головного меню
        self.copy_message_label = None  # Мітка для повідомлення про копіювання (якщо потрібно)

    def create_main_menu(self):
        # Сховуємо головне вікно меню
        self.main_menu.withdraw()

        # Створюємо нове вікно для операції
        self.gui_menu = Toplevel()
        self.gui_menu.title(self.operation_name)  # Назва вікна - назва операції
        self.gui_menu.config(bg="#2e2e38")  # Фон вікна
        self.gui_menu.resizable(False, False)  # Забороняємо змінювати розмір вікна

        # Створення фрейму для меню
        frame_menu = Frame(self.gui_menu, highlightbackground='#424256', highlightthickness=2, bg="#2e2e38")
        frame_menu.pack(fill=BOTH, expand=True, padx=10, pady=10)
        frame_menu.pack_propagate(False)  # Не дозволяємо фрейму змінювати розмір
        frame_menu.config(width=300, height=200)  # Встановлюємо конкретні розміри фрейму

        # Мітка для вибору розміру матриці
        Label(frame_menu, text='Виберіть розмір матриці:', font=('Helvetica', 12, 'bold'), bg="#2e2e38",
              fg="white").pack(pady=15)

        # Фрейм для налаштувань розміру матриці
        size_frame = Frame(frame_menu, bg="#2e2e38")
        size_frame.pack(pady=10)

        # Встановлюємо значення рядків та стовпців за замовчуванням
        self.rows, self.cols = tk.IntVar(value=3), tk.IntVar(value=3)
        size_options = [2, 3, 4, 5]  # Доступні опції для кількості рядків і стовпців

        # Створення меню для вибору кількості рядків
        row_menu = tk.OptionMenu(size_frame, self.rows, *size_options)
        row_menu.config(bg="#3b3b45", fg="white", font=('Helvetica', 10))
        row_menu.pack(side="left", padx=5)

        # Мітка для розділення рядків та стовпців
        Label(size_frame, text='x', font=('Helvetica', 12), bg="#2e2e38", fg="white").pack(side="left")

        # Створення меню для вибору кількості стовпців
        col_menu = tk.OptionMenu(size_frame, self.cols, *size_options)
        col_menu.config(bg="#3b3b45", fg="white", font=('Helvetica', 10))
        col_menu.pack(side="left", padx=5)

        # Фрейм для кнопок
        button_frame = Frame(frame_menu, bg="#2e2e38")
        button_frame.pack(pady=20)

        # Кнопка для переходу до введення матриці
        Button(button_frame, text="Ввести", font=('Helvetica', 11, 'bold'), command=self.open_input_window,
               bg="#4CAF50", fg="white", padx=20, pady=8, relief="raised", bd=2).pack()

    def open_input_window(self):
        # Сховуємо попереднє вікно меню
        self.gui_menu.withdraw()

        # Створюємо нове вікно для введення матриць
        self.gui_input = Toplevel()
        self.gui_input.title(f"{self.operation_name} Введення")
        self.gui_input.config(bg="#1e1e2f")

        # Розраховуємо розміри вікна залежно від кількості рядків та стовпців
        base_width, base_height = 420, 420
        extra_width = (self.cols.get() - 3) * 60  # Додаємо ширину залежно від кількості стовпців
        extra_height = (self.rows.get() - 3) * 40  # Додаємо висоту залежно від кількості рядків
        height_padding = 80 if self.rows.get() >= 5 else 0  # Додаємо додаткову висоту, якщо рядків більше або рівно 5
        width = base_width + extra_width  # Загальна ширина вікна
        height = base_height + extra_height + height_padding  # Загальна висота вікна
        self.gui_input.geometry(f"{width}x{height}")  # Встановлюємо розмір вікна
        self.gui_input.resizable(False, False)  # Забороняємо змінювати розмір вікна

        # Створення фрейму для введення
        frame_input = Frame(self.gui_input, highlightbackground='#3c3c4e', highlightthickness=2, bg="#1e1e2f")
        frame_input.pack(fill=BOTH, expand=True, padx=15, pady=15)

        # Налаштовуємо кількість стовпців для сітки
        frame_input.grid_columnconfigure(0, weight=1)
        frame_input.grid_columnconfigure(self.cols.get() + 1, weight=1)

        # Створення поля для введення елементів матриці A
        self.build_input_matrix(self.matrix_a, "Матриця A", frame_input, start_row=1, matrix_index=0)

        # Якщо потрібно, додаємо поле для введення елементів матриці B
        if not self.single_matrix:
            self.build_input_matrix(self.matrix_b, "Матриця B", frame_input, start_row=self.rows.get() + 3,
                                    matrix_index=1)

        # Фрейм для кнопок
        button_frame = Frame(frame_input, bg="#1e1e2f")
        button_frame.grid(row=self.rows.get() * 2 + (0 if self.single_matrix else 3) + 1, column=0,
                          columnspan=self.cols.get() + 2, pady=15)

        # Стиль кнопок
        button_style = {
            'font': ('Helvetica', 10, 'bold'),
            'fg': 'white',
            'padx': 8,
            'pady': 10,
            'width': 12,
            'relief': 'raised'
        }

        # Кнопка для вставлення значень з буфера обміну в матрицю A
        Button(button_frame, text="Вставити в A", command=lambda: self.paste_from_clipboard(self.matrix_a),
               bg="#5b9cd6", **button_style).grid(row=0, column=0, padx=5, pady=5)

        # Якщо дві матриці, додаємо кнопку для вставлення значень в матрицю B
        if not self.single_matrix:
            Button(button_frame, text="Вставити в B", command=lambda: self.paste_from_clipboard(self.matrix_b),
                   bg="#5b9cd6", **button_style).grid(row=0, column=1, padx=5, pady=5)

        # Кнопка для очищення матриць
        Button(button_frame, text="Очистити", command=self.clear_matrices, bg="#d9534f", **button_style).grid(row=0,
                                                                                                              column=2,
                                                                                                              padx=5,
                                                                                                              pady=5)

        # Кнопка для заповнення матриць випадковими значеннями
        Button(button_frame, text="Випадкові", command=self.fill_with_random_values, bg="#f0953a", **button_style).grid(
            row=1, column=0, padx=5, pady=5)

        # Кнопка для обчислення результату
        Button(button_frame, text="Обчислити", command=self.calculate_result, bg="#249c40", **button_style).grid(row=1,
                                                                                                                 column=1,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        # Кнопка для повернення до головного меню
        Button(button_frame, text="Назад", command=self.back_to_menu, bg="#5f5f75", **button_style).grid(row=1,
                                                                                                         column=2,
                                                                                                         padx=5, pady=5)

    def fill_with_random_values(self):
        # Генеруємо випадкові значення для матриці A
        random_matrix_a = np.random.randint(1, 10, (self.rows.get(), self.cols.get()))
        for i, row in enumerate(random_matrix_a):
            for j, value in enumerate(row):
                self.matrix_a[i][j].set(value)

        # Якщо використовується друга матриця, генеруємо випадкові значення для неї також
        if not self.single_matrix:
            random_matrix_b = np.random.randint(1, 10, (self.rows.get(), self.cols.get()))
            for i, row in enumerate(random_matrix_b):
                for j, value in enumerate(row):
                    self.matrix_b[i][j].set(value)

    def build_input_matrix(self, matrix, label_text, frame, start_row, matrix_index):
        # Створення мітки для матриці з заданим текстом (A або B) і стильовими налаштуваннями
        label = Label(frame, text=label_text, font=('Courier New', 12, 'bold'), bg="#2e2e38", fg="#a0a0b8")
        label.grid(row=start_row, column=1, columnspan=self.cols.get(), pady=5, sticky='ew')

        # Очищення існуючого списку елементів матриці
        matrix.clear()

        # Очищення списків віджетів введення для кожної матриці (A або B)
        if matrix_index == 0:
            self.entry_widgets_a.clear()
        else:
            self.entry_widgets_b.clear()

        # Створення полів введення для кожного елемента матриці
        for i in range(self.rows.get()):
            row = []
            for j in range(self.cols.get()):
                entry_var = StringVar()  # Змінна для збереження значення елемента матриці
                # Налаштування поля введення з відповідними параметрами для стилю та розміщення
                entry = Entry(
                    frame,
                    textvariable=entry_var,
                    width=6,
                    justify='center',
                    font=tkfont.Font(family="Courier New", size=12, weight="bold"),
                    relief="flat",
                    bg="#3a3a4f",
                    fg="#c9d1d9",
                    bd=1,
                    highlightthickness=2,
                    highlightbackground="#525269",
                    highlightcolor="#73738b"
                )
                entry.grid(row=start_row + i + 1, column=j + 1, padx=3, pady=3)
                # Додаємо обробник події для переходу по полям введення за допомогою клавіші Enter
                entry.bind("<Return>", lambda event, row=i, col=j, index=matrix_index: self.move_focus(row, col, index))

                row.append(entry_var)  # Додаємо змінну для кожного елемента до рядка

                # Додаємо поле введення у відповідний список віджетів (для матриці A або B)
                if matrix_index == 0:
                    self.entry_widgets_a.append(entry)
                else:
                    self.entry_widgets_b.append(entry)

            matrix.append(row)  # Додаємо сформований рядок до матриці

    def move_focus(self, row, col, matrix_index):
        # Переміщуємо фокус на наступне поле введення в рядку, якщо можливо.
        next_col = col + 1  # Наступна колонка
        next_row = row  # Поточний рядок

        max_cols = self.cols.get()  # Максимальна кількість колонок

        # Якщо ми досягли кінця рядка, переходимо на початок наступного рядка
        if next_col >= max_cols:
            next_col = 0
            next_row += 1

        # Якщо працюємо з першою матрицею
        if matrix_index == 0:
            # Переміщення фокусу в межах матриці A
            if next_row < self.rows.get():
                idx = next_row * max_cols + next_col
                self.entry_widgets_a[idx].focus_set()
        else:
            # Переміщення фокусу в межах матриці B
            if next_row < self.rows.get():
                idx = next_row * max_cols + next_col
                self.entry_widgets_b[idx].focus_set()

    def move_focus(self, row, col, matrix_index):
        # Альтернативний метод переміщення фокусу для іншої логіки переходу між матрицями.
        next_col = col + 1  # Наступна колонка
        next_row = row  # Поточний рядок

        max_rows = self.rows.get()  # Максимальна кількість рядків
        max_cols = self.cols.get()  # Максимальна кількість колонок

        # Переходимо на початок наступного рядка, якщо досягнуто кінця поточного рядка
        if next_col >= max_cols:
            next_col = 0
            next_row += 1

        # Якщо працюємо з першою матрицею (matrix_index == 0)
        if matrix_index == 0:
            if next_row < max_rows:
                # Переміщення фокусу в межах матриці A
                self.entry_widgets_a[next_row * max_cols + next_col].focus_set()
            elif not self.single_matrix:
                # Якщо є друга матриця, переносимо фокус на перше поле в матриці B
                self.entry_widgets_b[0].focus_set()
        else:
            if next_row < max_rows:
                # Переміщення фокусу в межах матриці B
                self.entry_widgets_b[next_row * max_cols + next_col].focus_set()
            else:
                # Після останнього елемента матриці B, переносимо фокус на початок матриці A
                self.entry_widgets_a[0].focus_set()

    # Стиль кнопок для інтерфейсу
    button_style = {
        'font': ('Helvetica', 9, 'bold'),  # Шрифт для тексту на кнопках
        'fg': 'white',  # Колір тексту
        'padx': 5,  # Відступ по горизонталі
        'pady': 5,  # Відступ по вертикалі
        'width': 10,  # Ширина кнопки
        'relief': 'raised'  # Стиль рамки кнопки
    }

    def paste_from_clipboard(self, matrix):
        try:
            # Отримуємо дані з буфера обміну та видаляємо зайві пробіли
            clipboard_data = self.gui_input.clipboard_get().strip()
            rows = clipboard_data.splitlines()  # Розбиваємо дані на рядки
            for i, row in enumerate(rows):
                if i < len(matrix):
                    values = row.split()  # Розбиваємо кожен рядок на окремі значення
                    for j, value in enumerate(values):
                        if j < len(matrix[i]):
                            matrix[i][j].set(value)  # Вставляємо значення в відповідне поле матриці
        except Exception as e:
            # Якщо виникла помилка, виводимо повідомлення про помилку
            messagebox.showerror("Помилка", f"Не вдалося вставити дані з буфера обміну:\n{e}")

    def clear_matrices(self):
        # Очищаємо всі елементи в обох матрицях
        for row in self.matrix_a:
            for entry in row:
                entry.set("")  # Очищаємо значення в полі введення для матриці A
        if not self.single_matrix:
            for row in self.matrix_b:
                for entry in row:
                    entry.set("")  # Очищаємо значення в полі введення для матриці B

    def calculate_result(self):
        try:
            # Перетворюємо значення з полів введення в цілі числа для матриці A
            matrix_a = [[int(cell.get()) for cell in row] for row in self.matrix_a]
            if not self.single_matrix:
                # Перетворюємо значення з полів введення в цілі числа для матриці B
                matrix_b = [[int(cell.get()) for cell in row] for row in self.matrix_b]

            # Перевірка, чи розміри матриць однакові для операцій з двома матрицями
            if not self.single_matrix and (len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0])):
                self.show_error_message("Матриці повинні бути одного розміру для складання.")
                return

            # Якщо працюємо з однією матрицею, виконуємо операцію над одною матрицею
            if self.single_matrix:
                self.result_matrix = self.perform_single_matrix_operation(matrix_a)
            else:
                # Якщо працюємо з двома матрицями, виконуємо відповідну операцію
                self.result_matrix = self.perform_two_matrix_operation(matrix_a, matrix_b)

            self.display_result()  # Відображаємо результат на екрані
        except ValueError:
            # Якщо введені некоректні дані (наприклад, не числа), виводимо повідомлення про помилку
            messagebox.showerror("Помилка", "Виявлено недопустимий ввід у матрицях.")

    def perform_single_matrix_operation(self, matrix):
        # Тут можна додати будь-яку операцію для однієї матриці, наприклад, транспонування чи обертання
        return matrix

    def perform_two_matrix_operation(self, matrix_a, matrix_b, operation_type="add"):
        # Вибір операції для двох матриць
        if operation_type == "add":
            # Додавання двох матриць
            return np.add(matrix_a, matrix_b).tolist()
        elif operation_type == "subtract":
            # Віднімання двох матриць
            return np.subtract(matrix_a, matrix_b).tolist()
        elif operation_type == "multiply":
            # Множення двох матриць
            return np.matmul(matrix_a, matrix_b).tolist()
        else:
            # Якщо тип операції не підтримується
            raise ValueError("Даний тип операції не підтримується.")

    def display_result(self):
        # Якщо є попередній графічний інтерфейс, видаляємо його
        if self.gui_input:
            self.gui_input.destroy()

        # Створюємо нове вікно для відображення результату
        self.gui_output = Toplevel()
        self.gui_output.title(f"{self.operation_name} Результат")
        self.gui_output.config(bg="#2e2e38")
        self.gui_output.resizable(False, True)

        # Фрейм для відображення результату
        frame_output = Frame(self.gui_output, highlightbackground='#424256', highlightthickness=2, bg="#2e2e38")
        frame_output.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Мітка з текстом "Результат"
        Label(frame_output, text="Результат:", font=('Helvetica', 12, 'bold'), bg="#2e2e38", fg="white").grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=len(
                                                                                                                  self.result_matrix[
                                                                                                                      0]),
                                                                                                              pady=10)

        # Відображаємо кожен елемент результатної матриці
        for i, row in enumerate(self.result_matrix):
            for j, value in enumerate(row):
                Label(
                    frame_output,
                    text=f"{value:^5}",
                    font=('Helvetica', 12),
                    bg="#2e2e38",
                    fg="white",
                    width=6,
                    anchor="center",
                ).grid(row=i + 1, column=j, padx=5, pady=5)

        # Фрейм для кнопок
        button_frame = Frame(frame_output, bg="#2e2e38")
        button_frame.grid(row=len(self.result_matrix) + 1, column=0, columnspan=len(self.result_matrix[0]), pady=10)

        # Кнопка для копіювання результату в буфер обміну
        copy_button = Button(button_frame, text="Копіювати результат", font=('Helvetica', 10),
                             command=self.copy_result_to_clipboard, bg="#5bc0de", fg="white", padx=10, pady=5, width=20)
        copy_button.grid(row=0, column=0, padx=5)

        # Кнопка для повернення в головне меню
        back_button = Button(button_frame, text="Назад", font=('Helvetica', 10), command=self.back_to_menu,
                             bg="#E57373", fg="white", padx=10, pady=5, width=20)
        back_button.grid(row=0, column=1, padx=5)

        # Створюємо лейбл для повідомлення про копіювання, якщо його ще немає
        if self.copy_message_label is None:
            self.copy_message_label = Label(frame_output, text="", font=('Helvetica', 10), bg="#2e2e38", fg="white")
            self.copy_message_label.grid(row=len(self.result_matrix) + 2, column=0,
                                         columnspan=len(self.result_matrix[0]), pady=5)

    def copy_result_to_clipboard(self):
        # Перетворюємо результат матриці в строку для копіювання
        result_str = '\n'.join(['\t'.join(map(str, row)) for row in self.result_matrix])

        # Очищаємо буфер обміну та додаємо новий результат
        self.gui_output.clipboard_clear()
        self.gui_output.clipboard_append(result_str)

        # Показуємо повідомлення про успішне копіювання
        self.show_copy_message("Результат скопійовано в буфер обміну.")

    def clear_copy_message(self):
        # Очищаємо повідомлення про копіювання
        self.copy_message_label.config(text="")
        self.copy_message_label.config(fg="white")

    def show_copy_message(self, message):
        # Показуємо повідомлення про копіювання
        if self.copy_message_label:
            self.copy_message_label.config(text=message, fg="#b0b0b0")
            self.animate_copy_message()  # Запускаємо анімацію повідомлення

    def animate_copy_message(self):
        # Запускаємо анімацію зміни кольору повідомлення
        self.copy_message_label.config(fg="#2e2e38")
        self.copy_message_label.after(100, self.fade_in)

    def fade_in(self):
        # Анімація зміни кольору повідомлення
        current_color = self.copy_message_label.cget("fg")
        if current_color != "white":
            # Обчислюємо новий колір для плавного переходу
            new_color = "#" + ''.join(
                format(int((int(current_color[1:3], 16) + 255) // 2), '02x') if i == 0 else format(
                    int(current_color[1:3], 16), '02x') for i in range(3))
            self.copy_message_label.config(fg=new_color)
            self.copy_message_label.after(100, self.fade_in)

    def fade_out(self):
        # Анімація зменшення яскравості кольору повідомлення
        current_color = self.copy_message_label.cget("fg")
        if current_color != "#b0b0b0":
            new_color = "#" + ''.join(format(int((int(current_color[1:3], 16) + 0) // 2, 'x'), '02') for c in range(3))
            self.copy_message_label.config(fg=new_color)
            self.copy_message_label.after(50, self.fade_out)
        else:
            # Коли колір досягає кінцевого значення, очищаємо повідомлення
            self.clear_copy_message()

    def back_to_menu(self):
        # Закриваємо вікно з результатом та повертаємо головне меню
        if self.gui_input:
            self.gui_input.destroy()
        if self.gui_output:
            self.gui_output.destroy()
        self.main_menu.deiconify()  # Показуємо головне меню
