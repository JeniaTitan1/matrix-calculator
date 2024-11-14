from tkinter import messagebox
import numpy as np
from src.matrix_operation import MatrixOperation


# Клас Trans наслідує MatrixOperation та відповідає за транспонування матриць
class Trans(MatrixOperation):
    def __init__(self, main_menu):
        # Ініціалізація класу з назвою "Транспонування" та встановленням одного вводу
        super().__init__("Транспонування", main_menu, single_matrix=True)

    # Основний метод для обчислення транспонованої матриці
    def calculate_result(self):
        try:
            # Отримуємо матрицю зі значеннями як цілі числа
            matrix = self.get_integer_matrix(self.matrix_a)
            # Виконуємо транспонування матриці
            self.result_matrix = np.transpose(matrix).tolist()
            # Відображаємо результат
            self.display_result()
        except ValueError as e:
            # Виводимо повідомлення про помилку у випадку неправильного вводу
            self.show_error_message("Invalid input in the matrix.")

    # Метод для отримання матриці з цілочисельними значеннями
    def get_integer_matrix(self, matrix_vars):
        return [[int(cell.get().strip()) for cell in row] for row in matrix_vars]

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
