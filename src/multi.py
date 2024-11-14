from matrix_operation import MatrixOperation
import numpy as np
from tkinter import messagebox


class Multi(MatrixOperation):
    def __init__(self, main_menu):
        # Ініціалізація класу з назвою "Множення" для операції множення матриць
        super().__init__("Множення", main_menu)

    def calculate_result(self):
        try:
            # Створюємо порожній список для матриці A
            matrix_a = []
            for row in self.matrix_a:
                matrix_a_row = []
                for cell in row:
                    value = cell.get().strip()  # Отримуємо значення з кожної клітинки
                    if not value.isdigit():  # Перевірка на числові значення
                        raise ValueError("Виявлено недопустимий ввід у матрицях.")
                    matrix_a_row.append(int(value))  # Додаємо число до рядка матриці
                matrix_a.append(matrix_a_row)  # Додаємо рядок до матриці

            # Створюємо порожній список для матриці B
            matrix_b = []
            for row in self.matrix_b:
                matrix_b_row = []
                for cell in row:
                    value = cell.get().strip()  # Отримуємо значення з кожної клітинки
                    if not value.isdigit():  # Перевірка на числові значення
                        raise ValueError("Виявлено недопустимий ввід у матрицях.")
                    matrix_b_row.append(int(value))  # Додаємо число до рядка матриці
                matrix_b.append(matrix_b_row)  # Додаємо рядок до матриці

            # Перевірка на сумісність розмірів матриць для множення
            if len(matrix_a[0]) != len(matrix_b):
                self.show_error_message("Матриці мають несумісні розміри для множення.")
                return

            # Виконання множення матриць
            self.result_matrix = np.matmul(matrix_a, matrix_b).tolist()
            self.display_result()  # Виведення результату

        except ValueError as e:
            # Виведення повідомлення про помилку при неправильному вводу
            self.show_error_message(str(e))

    def show_error_message(self, message):
        # Метод для виведення повідомлення про помилку
        messagebox.showerror("Помилка", message)

    def clear_windows(self):
        # Метод для очищення вікон вводу та виводу
        if self.gui_input:
            self.gui_input.destroy()
        if self.gui_output:
            self.gui_output.destroy()

    def back_to_menu(self):
        # Метод для повернення в головне меню
        self.clear_windows()
        self.main_menu.deiconify()
