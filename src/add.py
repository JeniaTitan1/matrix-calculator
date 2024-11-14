from tkinter import messagebox
from src.matrix_operation import MatrixOperation
import numpy as np


# Клас Add наслідує MatrixOperation та відповідає за додавання двох матриць
class Add(MatrixOperation):
    def __init__(self, main_menu):
        # Ініціалізація класу з назвою "Додавання"
        super().__init__("Додавання", main_menu)

    # Основний метод для обчислення суми двох матриць
    def calculate_result(self):
        try:
            # Отримуємо дві матриці з цілими числами
            matrix_a = self.get_integer_matrix(self.matrix_a)
            matrix_b = self.get_integer_matrix(self.matrix_b)

            # Перевірка, чи матриці мають однаковий розмір
            if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
                self.show_error_message("Матриці повинні бути одного розміру для складання.")
                return

            # Додаємо дві матриці та перетворюємо результат у список
            self.result_matrix = np.add(matrix_a, matrix_b).tolist()
            # Відображаємо результат
            self.display_result()

        except ValueError:
            # Виводимо повідомлення про помилку у випадку неправильного вводу
            self.show_error_message("Виявлено недопустимий ввід у матрицях.")

    # Метод для отримання матриці з цілочисельними значеннями
    def get_integer_matrix(self, matrix_vars):
        return [[int(cell.get()) for cell in row] for row in matrix_vars]

    # Метод для виведення повідомлення про помилку
    def show_error_message(self, message):
        messagebox.showerror("Помилка", message)

    # Метод для очищення вікон вводу та виводу
    def clear_windows(self):
        if self.gui_input:
            self.gui_input.destroy()
        if self.gui_output:
            self.gui_output.destroy()

    # Метод для повернення в головне меню
    def back_to_menu(self):
        self.clear_windows()
        self.main_menu.deiconify()
