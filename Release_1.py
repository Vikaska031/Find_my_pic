import streamlit as st
import os
import random
from PIL import Image

# Путь к папке с изображениями
image_folder = "/home/viktorya/Рабочий стол/find_my pic/photo"

# Получаем список файлов из папки с изображениями
image_files = [f for f in os.listdir(image_folder) if f.endswith((".jpg", ".jpeg", ".png"))]

def get_random_images(num_images):
    # Выбираем случайные изображения из списка
    random_images = random.sample(image_files, num_images)
    return random_images

def main():
    image_path = os.path.join(image_folder, "/home/viktorya/Рабочий стол/find_my pic/Без имени.jpeg")
    image = Image.open(image_path)

    # Создаем две колонки для размещения заголовка и изображения
    col1, col2 = st.columns([1, 3])  

    with col1:
        st.title("Find my pic!")

    with col2:
        st.image(image, use_column_width=True)  

       # Получаем  запрос от пользователя
    user_input = st.text_input("Введите текстовый запрос:", "")

    # Получаем количество изображений от пользователя
    num_images = st.number_input("Выберите количество изображений", min_value=1, max_value=len(image_files), value=5, step=2)

    if st.button("Поиск изображений"):
        # Генерируем случайные изображения
        random_images = get_random_images(num_images)

        st.write("Наиболее подходящие изображения:")

        # Итерируемся попарно по списку изображений
        for i in range(0, len(random_images), 2):
            col1, col2 = st.columns(2)  # Создаем две колонки для вывода изображений
            image_path1 = os.path.join(image_folder, random_images[i])
            image_path2 = os.path.join(image_folder, random_images[i+1])
            image1 = Image.open(image_path1)
            image2 = Image.open(image_path2)
            with col1:
                st.image(image1, use_column_width=True)  
            with col2:
                st.image(image2, use_column_width=True)  

if name == "main":
    main()