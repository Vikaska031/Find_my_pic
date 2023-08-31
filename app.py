import streamlit as st
# print(st.__version__)
from PIL import Image
import pandas as pd
import torch
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
import os
import zipfile


# Пути (господни)
zip_path = 'flickr30k_images.zip'
capturings_path = 'results.csv'
model_weights_path = 'text_features.pt'
images_path = 'flickr30k_images/' # в случае архива его надо распоковать, делаю это далее по коду

# Кэширование загрузки модели и других дорогостоящих операций
@st.cache_resource
# @st.cache
def load_model():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

@st.cache_data
# @st.cache
def load_data(capturings_path, grouped_path):
    df = pd.read_csv(capturings_path, sep='|')
    grouped_df = pd.read_csv(grouped_path)
    return df, grouped_df

@st.cache_data
# @st.cache
def load_text_features(text_features_path):
    return torch.load(text_features_path)

def unpack_images(zip_path):
    if not os.path.exists(images_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')


# Инкапсулируем логику в функции
def find_images(query, top, text_features, df, grouped_df):
    # Векторизация текстового запроса
    model, processor = load_model()
    query_input = processor(query, return_tensors="pt")
    query_features = model.get_text_features(**query_input)

    # Поиск самых похожих изображений
    similarity_scores = cosine_similarity(query_features.detach().numpy(), text_features.detach().numpy())
    top_indices = similarity_scores.argsort()[0][-top:][::-1]
    top_images = df.loc[top_indices, 'image_name'].tolist()
    top_similarity_scores = similarity_scores[0][top_indices]
    
    top_images_df = pd.DataFrame({'image_name': top_images})
    top_info = pd.merge(top_images_df, grouped_df, on='image_name')
    
    return top_images, top_similarity_scores, top_info


# Основная программа
if __name__ == '__main__':
    st.title("Find my pic!")

    images_path = 'flickr30k_images/' # в случае архива его надо распоковать, делаю это далее по коду

    # Загрузка модели и данных
    model, processor = load_model()
    df, grouped_df = load_data('results.csv', 'grouped_df.csv')
    text_features = load_text_features('text_features.pt')

    # Ввод данных пользователем
    user_input = st.text_input("Введите текстовый запрос:", "")
    num_images = st.number_input("Выберите количество изображений", min_value=1, max_value=10, value=5, step=1)

    # Объявляем эти переменные заранее, чтобы избежать NameError
    top_images = []
    top_similarity_scores = []

    unpack_images('flickr30k_images.zip')
    
    
    if st.button("Поиск изображений"):

        
        
        top_images, top_similarity_scores, top_info = find_images(user_input, num_images, text_features, df, grouped_df)

    # Вывод найденных изображений и подписей
    for index, (img_name, score) in enumerate(zip(top_images, top_similarity_scores)):
        comment = top_info.loc[top_info['image_name'] == img_name, ' comment'].values[0]
    
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"Image filename: {img_name}")
            st.write(f"Image capture: {comment}")
            st.write(f"Model confidence of pic relevance: {score:.4f}")
    
        with col2:
            # Загружаем только нужные изображения
            # img_path = os.path.join(images_path, 'path_within_zip', img_name)  # уточните путь внутри zip-архива
            img_path = os.path.join(images_path, img_name)  # уточните путь внутри zip-архива 
            st.image(Image.open(img_path), use_column_width=True)