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
threshold = 210


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
    with open((os.path.splitext(filename)[0] + '.c'), "r") as f:
        text = f.read()
    lines = text.splitlines()
    selected_lines = lines[0:34]
    txt_widget = tk.Text(root)
    txt_widget.pack(fill="both", expand=True)
    for line in selected_lines:
        txt_widget.insert("end", line + "\n")


def click_button():
    threshold = int(threshold_entry.get())
    convert()
    print_result()

root = tk.Tk()
root.geometry("1000x600")
root.withdraw()

filename = filedialog.askopenfilename()
name, extension = os.path.splitext(str(filename))
print(extension)
if extension.lower() != ".bmp":
    messagebox.showerror("Ошибка!", "Файл должен быть:\n\n - с расширением .bmp\n - c разрешением 122х32")
    exit()

root.deiconify()
convert()
print_result()
btn = ttk.Button(text="Еще раз", command=click_button)
btn.pack()
threshold_entry = ttk.Entry()
threshold_entry.pack(anchor="s", padx=8, pady= 8)
root.mainloop()
