from tkinter import messagebox
from numpy.linalg import LinAlgError, inv
from src.matrix_operation import MatrixOperation

# Клас Inverse наслідує MatrixOperation та відповідає за знаходження оберненої матриці
class Inverse(MatrixOperation):
    def __init__(self, main_menu):
        # Ініціалізація класу з назвою "Inverse" для операції з однією матрицею
        super().__init__("Inverse", main_menu, single_matrix=True)

    # Основний метод для обчислення оберненої матриці
    def calculate_result(self):
        try:
            # Отримуємо матрицю з числами типу float
            matrix = self.get_float_matrix(self.matrix_a)

            # Перевірка, чи матриця є квадратною
            if len(matrix) != len(matrix[0]):
                self.show_error_message("Матриця повинна бути квадратною для знаходження оберненої.")
                return

            # Знаходимо обернену матрицю та округлюємо значення до двох знаків після коми
            self.result_matrix = [[round(value, 2) for value in row] for row in inv(matrix).tolist()]
            # Відображаємо результат
            self.display_result()

        except LinAlgError:
            # Виводимо повідомлення про помилку, якщо оберненої матриці не існує
            self.show_error_message("Матриця не є оберненою.")
        except ValueError:
            # Виводимо повідомлення про помилку у випадку неправильного вводу
            self.show_error_message("Виявлено недопустимий ввід у матриці.")

    # Метод для отримання матриці з числами типу float
    def get_float_matrix(self, matrix_vars):
        return [[float(cell.get()) for cell in row] for row in matrix_vars]

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
