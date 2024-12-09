import tkinter as tk

# Алгоритмы
def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1
    points = []
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return points

def bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    err = dx - dy

    x, y = x1, y1
    points = []
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points

def bresenham_circle(xc, yc, r):
    x, y = 0, r
    d = 3 - 2 * r
    points = []

    while x <= y:
        points += [(xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
                   (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)]
        if d <= 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    return points

# Интерфейс
class RasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы растеризации")

        # Размер окна
        self.root.geometry("1200x800")
        self.scale = 20  # Базовый размер клетки в пикселях
        self.offset_x = 0
        self.offset_y = 0

        # Цветовая схема
        self.bg_color = "#2E3440"  # Темный фон
        self.fg_color = "#ECEFF4"  # Светлый текст
        self.button_color = "#4C566A"  # Цвет кнопок
        self.canvas_bg = "#D8DEE9"  # Светлый фон холста

        self.root.configure(bg=self.bg_color)

        # Canvas
        self.canvas = tk.Canvas(root, bg=self.canvas_bg)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Панель управления
        self.control_frame = tk.Frame(root, bg=self.bg_color)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)

        # Поля ввода координат
        self.create_input_fields()

        # Кнопки
        self.add_controls()

        # Поддержка перетаскивания
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.do_pan)

        # Поддержка масштабирования
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.redraw()

    def create_input_fields(self):
        label_style = {"bg": self.bg_color, "fg": self.fg_color, "font": ("Arial", 10)}

        # Поля для ввода координат
        tk.Label(self.control_frame, text="X1:", **label_style).pack(anchor="w")
        self.x1_entry = tk.Entry(self.control_frame)
        self.x1_entry.pack(fill=tk.X, pady=2)

        tk.Label(self.control_frame, text="Y1:", **label_style).pack(anchor="w")
        self.y1_entry = tk.Entry(self.control_frame)
        self.y1_entry.pack(fill=tk.X, pady=2)

        tk.Label(self.control_frame, text="X2:", **label_style).pack(anchor="w")
        self.x2_entry = tk.Entry(self.control_frame)
        self.x2_entry.pack(fill=tk.X, pady=2)

        tk.Label(self.control_frame, text="Y2:", **label_style).pack(anchor="w")
        self.y2_entry = tk.Entry(self.control_frame)
        self.y2_entry.pack(fill=tk.X, pady=2)

        tk.Label(self.control_frame, text="Радиус (для окружности):", **label_style).pack(anchor="w")
        self.radius_entry = tk.Entry(self.control_frame)
        self.radius_entry.pack(fill=tk.X, pady=2)

    def add_controls(self):
        button_style = {
            "bg": self.button_color,
            "fg": self.fg_color,
            "activebackground": "#3B4252",
            "activeforeground": self.fg_color,
            "relief": tk.RAISED,
            "font": ("Arial", 12),
        }

        tk.Button(
            self.control_frame, text="ЦДА", command=self.run_dda, **button_style
        ).pack(fill=tk.X, pady=5)
        tk.Button(
            self.control_frame,
            text="Брезенхем (отрезок)",
            command=self.run_bresenham,
            **button_style,
        ).pack(fill=tk.X, pady=5)
        tk.Button(
            self.control_frame,
            text="Брезенхем (окружность)",
            command=self.run_circle,
            **button_style,
        ).pack(fill=tk.X, pady=5)
        tk.Button(
            self.control_frame, text="Очистить", command=self.clear_canvas, **button_style
        ).pack(fill=tk.X, pady=5)

    def run_dda(self):
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
            points = dda(x1, y1, x2, y2)
            self.draw_points(points, color="blue")
        except ValueError:
            print("Введите корректные значения для координат.")

    def run_bresenham(self):
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
            points = bresenham(x1, y1, x2, y2)
            self.draw_points(points, color="green")
        except ValueError:
            print("Введите корректные значения для координат.")

    def run_circle(self):
        try:
            xc = int(self.x1_entry.get())
            yc = int(self.y1_entry.get())
            r = int(self.radius_entry.get())
            points = bresenham_circle(xc, yc, r)
            self.draw_points(points, color="red")
        except ValueError:
            print("Введите корректные значения для центра и радиуса.")

    def draw_points(self, points, color="black"):
        for x, y in points:
            x_scaled = x * self.scale + self.offset_x + self.canvas.winfo_width() // 2
            y_scaled = y * self.scale + self.offset_y + self.canvas.winfo_height() // 2
            self.canvas.create_oval(
                x_scaled - 2, y_scaled - 2, x_scaled + 2, y_scaled + 2, fill=color
            )

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()

    def draw_grid(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cx = width // 2 + self.offset_x
        cy = height // 2 + self.offset_y

        # Вертикальные линии
        for x in range(-width // 2, width // 2, self.scale):
            x_screen = x + cx
            self.canvas.create_line(x_screen, 0, x_screen, height, fill="#AAAAAA")
            if abs(x) % (5 * self.scale) == 0:
                self.canvas.create_text(x_screen, cy, text=str((x - cx) // self.scale), fill="black")

        # Горизонтальные линии
        for y in range(-height // 2, height // 2, self.scale):
            y_screen = y + cy
            self.canvas.create_line(0, y_screen, width, y_screen, fill="#AAAAAA")
            if abs(y) % (5 * self.scale) == 0:
                self.canvas.create_text(cx, y_screen, text=str((y - cy) // self.scale), fill="black")

        # Оси
        self.canvas.create_line(cx, 0, cx, height, fill="black", width=2)
        self.canvas.create_line(0, cy, width, cy, fill="black", width=2)

    def start_pan(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def do_pan(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.offset_x += dx
        self.offset_y += dy
        self.start_x = event.x
        self.start_y = event.y
        self.redraw()

    def zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.scale = max(5, self.scale * scale_factor)  # Минимальный масштаб - 5 пикселей
        self.redraw()

    def redraw(self):
        self.clear_canvas()
        self.draw_grid()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = RasterApp(root)
    root.mainloop()
