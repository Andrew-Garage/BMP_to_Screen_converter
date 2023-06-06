# Cкрипт преобразует BMP-изображение в массив байтов, который можно использовать для отображения изображения на
# устройствах с ограниченными ресурсами, таких как микроконтроллеры или дисплеи с маленьким разрешением.
# Результат сохраняется в новый файл с расширением ".c" и содержит массив констант типа unsigned char.

#       ("C:\\Users\\PC\\Desktop\\fault.bmp")

from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from sys import exit

# Переменная порога градации серого. Меньше значение переменной - меньше деталей.
threshold = 120
# txt_widget = None


def convert():
    # Открываем BMP-изображение
    # filename = "C:\\Users\\PC\\Desktop\\fault3.bmp"
    image = Image.open(filename)

    # Преобразуем изображение в градации серого
    image = image.convert("L")

    # Получаем данные о размере изображения
    width, height = image.size

    # Создаем двухмерный массив для хранения значений пикселей
    pixels = []
    picture = []

    # Обрабатываем каждый пиксель изображения
    for y in range(height):
        row = []
        pic_row = []
        for x in range(width):
            # Получаем значение яркости пикселя (от 0 до 255)
            brightness = image.getpixel((x, y))
            # Добавляем значение яркости в текущую строку. Инверсия пикселей по яркости.
            if brightness <= threshold:
                row.append(1)
                pic_row.append('@')
            else:
                row.append(0)
                pic_row.append(' ')
        # Добавляем строку в массив пикселей
        # print(pic_row)
        pixels.append(row)
        picture.append(pic_row)

    # with open("C:\\Users\\PC\\Desktop\\Blokir122_32.c", "w") as f:
    with open((os.path.splitext(filename)[0] + '.c'), "w") as f:
        f.write('/*' + "\n")
        for b in picture:
            f.write("".join(b) + "\n")
            print("".join(b) + "\n")
        f.write('*/' + "\n\n\n")

        f.write('const unsigned char Blokir[488] = {\n')
    # Разбиваем массив на полоски по 8 строк
        byte_rows = [pixels[i:i+8] for i in range(0, len(pixels), 8)]

        # Преобразуем каждую полоску в последовательность байтов и сохраняем в файле
        for byte_row in byte_rows:
            for x in range(width):
                mybyte = []
                for row in byte_row:
                    # print(row[x])
                    mybyte.append(row[x])
                # print(mybyte) # прямые байты
                mybyte = mybyte[::-1]
                # print(mybyte)   #инвертированные байты
                hex_str = ''
                for i in range(0, len(mybyte), 4):
                    nibble = mybyte[i:i + 4]
                    hex_digit = hex(int(''.join(map(str, nibble)), 2))[2:].upper()
                    hex_str += hex_digit
                # print('0x' + hex_str)
                f.write('0x' + hex_str + ', \n')

            print()
        f.write('}; \n')


def print_result():
    global txt_widget
    with open((os.path.splitext(filename)[0] + '.c'), "r") as f:
        text = f.read()
    lines = text.splitlines()
    selected_lines = lines[0:34]
    # txt_widget = tk.Text(root)
    # txt_widget.pack(fill="both", expand=True)
    txt_widget.delete("1.0", "end")
    for line in selected_lines:
        txt_widget.insert("end", line + "\n")


def push_enter(event):
    click_button()

def click_button():
    global threshold
    threshold_str = threshold_entry.get()
    if threshold_str.isdigit():
        if int(threshold_str) < 256:
            threshold = int(threshold_str)
        else:
            threshold = 100
            threshold_value.set(str(threshold))
            ttk.Entry(root, textvariable=threshold_value)
            messagebox.showwarning("Предупреждение!", "Число должно быть от 0 до 255")
    else:
        threshold = 100
        threshold_value.set(str(threshold))
        ttk.Entry(root, textvariable=threshold_value)
        messagebox.showwarning("Предупреждение!", "Число должно быть от 0 до 255")
    convert()
    print_result()
    print(threshold)


def click_button_down():
    global threshold
    threshold = threshold - 1
    threshold_value.set(str(threshold))
    threshold_entry = ttk.Entry(root, textvariable=threshold_value)


def click_button_up():
    global threshold
    threshold = threshold + 1
    threshold_value.set(str(threshold))
    threshold_entry = ttk.Entry(root, textvariable=threshold_value)


root = tk.Tk()
root.geometry("1000x700")
root.withdraw()

txt_widget = tk.Text(root)
txt_widget.pack(fill="both", expand=True)

filename = filedialog.askopenfilename()
name, extension = os.path.splitext(str(filename))
print(extension)
if extension.lower() != ".bmp":
    messagebox.showerror("Ошибка!", "Файл должен быть:\n\n - с расширением .bmp\n - c разрешением 122х32")
    exit()

root.deiconify()
convert()
print_result()
btn_up = ttk.Button(text="+ 1", command=click_button_up)
btn_up.pack()
btn = ttk.Button(text="Обновить", command=click_button)
btn.pack()
btn_down = ttk.Button(text="- 1", command=click_button_down)
btn_down.pack()

threshold_value = tk.StringVar()
threshold_value.set(str(threshold))
threshold_entry = ttk.Entry(root, textvariable=threshold_value)
threshold_entry.pack(anchor="s", padx=8, pady=4)

root.bind('<Return>', push_enter)
root.mainloop()
