import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def putpixel(img, x, y, r, g, b):
    """
    Получает прямой доступ к матрице пикселей и устанавливает цвет.
    """
    pixels = img.load()  
    pixels[x, y] = (r, g, b)  


class Images:

    def __init__(self):
        self.img = None
        self.tk_img = None

    def add_tasc(self):
        "функция раскрашивает точки по варианту 9"
        if self.img:
            img = self.img.convert("RGB")
            w, h = img.size
            
            putpixel(img, 0, 0, 64, 64, 64)
            putpixel(img, w - 1, 0, 255, 64, 64)
            putpixel(img, w - 1, h // 2, 64, 255, 64)
            
            self.img = img
            return True
        return False

images = Images()


def load_image():
    "функция читает файл"
    filename = filedialog.askopenfilename(title="Выбрать файл", filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
    if filename:
        images.img = Image.open(filename)
        update_display()

def save_image():
    "функция записывает файл"
    if not images.img:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
    if images.img:
        filename = filedialog.asksaveasfilename(title="Сохранить как", defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if filename:
            images.img.save(filename)
            messagebox.showinfo("Успех", "Файл сохранен!")
            return
    messagebox.showerror("Ошибка", f"Не удалось сохранить файл.")
            

def save_pbm():
    "функция записывает файл в формате PBM"
    if not images.img:
        messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
        return
        
    filename = filedialog.asksaveasfilename(
        title="Сохранить как PBM", 
        defaultextension=".pbm", 
        filetypes=[("PBM (черно-белый)", "*.pbm")]
    )
    if filename:
        try:
 
            pbm_img = images.img.convert("1")
            width, height = pbm_img.size
            pixels = pbm_img.load()
            
            with open(filename, 'w') as f:
                # Заголовок PBM файла
                f.write("P1\n")
                f.write(f"{width} {height}\n")
                
                # Записываем пиксели (0 = белый, 1 = черный)
                for y in range(height):
                    row = []
                    for x in range(width):
                        pixel = pixels[x, y]
                        row.append("0" if pixel == 255 else "1")
                    f.write(" ".join(row) + "\n")
            
            messagebox.showinfo("Успех", "Файл сохранен в PBM!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")



def apply_color():
    "функция применяет раскрашивание и обновляет экран"
    if images.add_tasc():
        update_display()

def update_display():
    "обновляет картинку на форме"
    if images.img:
        display_img = images.img.copy()
        display_img.thumbnail((500, 400)) # Масштабируем для окна
        images.tk_img = ImageTk.PhotoImage(display_img)
        image_label.config(image=images.tk_img)


root = tk.Tk()
root.title("Обработка изображений")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn_load = tk.Button(button_frame, text="Загрузить картинку", command=load_image)
btn_load.pack(side=tk.LEFT, padx=5)

btn_color = tk.Button(button_frame, text="Раскрасить точки", command=apply_color)
btn_color.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(button_frame, text="Сохранить PNG/JPG", command=save_image)
btn_save.pack(side=tk.LEFT, padx=5)

btn_save_pbm = tk.Button(button_frame, text="Сохранить PBM", command=save_pbm)
btn_save_pbm.pack(side=tk.LEFT, padx=5)

# Изображение-заглушку
placeholder = Image.new("RGB", (500, 400), (240, 240, 240))
images.tk_img = ImageTk.PhotoImage(placeholder)

# Метка для отображения изображения
image_label = tk.Label(root, image=images.tk_img, bg="lightgray", relief="sunken")
image_label.pack(padx=10, pady=10)

root.mainloop()