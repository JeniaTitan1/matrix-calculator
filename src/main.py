from tkinter import Tk, Button, Frame, Label

# Імпортуємо класи для операцій з матрицями: додавання, множення, транспонування та обернена матриця
from src.multi import Multi
from add import Add
from trans import Trans
from inverse import Inverse


class Menu:
    def __init__(self):
        # Ініціалізуємо головне вікно Tkinter для меню
        self.gui_menu = Tk()
        self.gui_menu.title("Enhanced Matrix Operations Menu")  # Назва вікна
        self.gui_menu.geometry("450x450")  # Розмір вікна
        self.gui_menu.configure(bg="#1e1e1e")  # Колір фону
        self.gui_menu.resizable(False, False)  # Забороняємо змінювати розмір вікна

        # Створюємо фрейм для розміщення кнопок меню
        self.frame_menu = Frame(self.gui_menu, bg="#2b2b2b", highlightthickness=1, highlightbackground="#444")
        self.frame_menu.place(relx=0.5, rely=0.5, anchor="center", width=320, height=350)

        # Створюємо заголовок для меню
        Label(
            self.frame_menu,
            text="Matrix Operations",  # Текст заголовка
            font=("Helvetica", 18, "bold"),  # Шрифт заголовка
            bg="#2b2b2b",  # Колір фону заголовка
            fg="white"  # Колір тексту
        ).pack(pady=(15, 25))  # Відступи для вертикального простору

        # Створюємо кнопки для різних операцій з матрицями (додавання, множення, транспонування, обернена матриця)
        self.create_button("Add (додати)", lambda: Add(self.gui_menu), "#3aaf76", "#2d8c5c")
        self.create_button("Multiply (Помножити)", lambda: Multi(self.gui_menu), "#4f83ff", "#3b5fd1")
        self.create_button("Transpose (Транспонувати)", lambda: Trans(self.gui_menu), "#ffb347", "#d1873b")
        self.create_button("Inverse (інвертувати)", lambda: Inverse(self.gui_menu), "#e85a71", "#b84357")

        # Запускаємо основний цикл Tkinter для відображення меню
        self.gui_menu.mainloop()

    def create_button(self, text, command, color1, color2):
        """
        Створює кнопку з вказаним текстом, командою і кольорами.
        Кнопка також має ефекти при наведенні для динамічного взаємодії.
        """
        button = Button(
            self.frame_menu,
            text=text,  # Текст на кнопці
            command=command,  # Команда, яка виконується при натисканні кнопки
            font=("Helvetica", 12, "bold"),  # Шрифт для тексту на кнопці
            fg="white",  # Колір тексту
            bg=color1,  # Початковий колір фону
            activebackground=color2,  # Колір фону при натисканні кнопки
            relief="flat",  # Плоский вигляд кнопки без бордера
            padx=20,  # Горизонтальні відступи
            pady=10,  # Вертикальні відступи
            cursor="hand2",  # Курсор у вигляді руки при наведенні
            borderwidth=0,  # Без межі
        )
        button.pack(fill="x", pady=8, padx=15)  # Розміщуємо кнопку з відступами та на всю ширину

        # Прив'язуємо ефекти наведеня на кнопку
        button.bind("<Enter>", lambda e: self.on_hover(button, color2, 1.15, 6))  # Коли миша заходить на кнопку
        button.bind("<Leave>", lambda e: self.on_hover(button, color1, 1.0, 0))  # Коли миша покидає кнопку

    def on_hover(self, button, color, target_scale, shadow_offset):
        """
        Обробляє ефекти при наведенні, такі як зміна розміру шрифту кнопки та зміна кольору фону.
        """
        self.animate_scale(button, target_scale, shadow_offset)  # Анімація зміни розміру шрифту
        button.config(bg=color)  # Зміна кольору фону кнопки

    def animate_scale(self, button, target_scale, shadow_offset):
        """
        Анімує зміну розміру шрифту на кнопці.
        Поступово змінює розмір шрифту до цільового з плавною анімацією.
        """
        # Отримуємо поточний розмір шрифту кнопки
        current_size = int(button["font"].split()[1])
        target_size = int(12 * target_scale)  # Обчислюємо цільовий розмір шрифту
        step = 1 if target_size > current_size else -1  # Визначаємо, чи збільшувати, чи зменшувати розмір шрифту

        # Анімуємо зміну розміру шрифту до досягнення цільового розміру
        if current_size != target_size:
            new_size = current_size + step
            button.config(font=(button["font"].split()[0], new_size, "bold"))  # Оновлюємо розмір шрифту
            button.config(highlightthickness=shadow_offset, highlightbackground="#444" if shadow_offset else None)
            button.after(10, lambda: self.animate_scale(button, target_scale,
                                                        shadow_offset))  # Рекурсивний виклик для продовження анімації


# Якщо файл запускається як основний, ініціалізуємо і запускаємо меню
if __name__ == "__main__":
    Menu()  # Ініціалізація та запуск меню
