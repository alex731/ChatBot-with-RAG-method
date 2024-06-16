import fitz  # PyMuPDF для работы с PDF файлами
import faiss  # FAISS для быстрого поиска по эмбеддингам
import numpy as np  # NumPy для работы с массивами

from sentence_transformers import SentenceTransformer  # SentenceTransformer для создания эмбеддингов текста

class PDFRetriever:
    def __init__(self, pdf_path, model_name='all-MiniLM-L6-v2', faiss_index_method='IndexFlatL2'):
        """
        Инициализация класса PDFRetriever.
        :param pdf_path: Путь к PDF файлу.
        :param model_name: Название модели для создания эмбеддингов.
        :param faiss_index_method: Метод FAISS для построения индекса.
        """
        self.pdf_path = pdf_path
        self.document = fitz.open(pdf_path)  # Открытие PDF файла
        self.index = None  # Индекс для поиска
        self.embeddings = []  # Список эмбеддингов для страниц(проверить по словам или предложениям)
        self.texts = []  # Список текстов страниц
        self.model = SentenceTransformer(model_name)  # Загрузка модели для создания эмбеддингов
        self.build_index(faiss_index_method)  # Построение индекса

    def build_index(self, faiss_index_method):
        """
        Создание эмбеддингов для каждой страницы PDF и построение индекса для поиска.
        """
        for page_num in range(len(self.document)):
            page = self.document.load_page(page_num)  # Загрузка страницы PDF
            text = page.get_text()  # Извлечение текста из страницы
            self.texts.append(text)  # Сохранение текста в список
            embedding = self.model.encode(text)  # Создание эмбеддинга для текста
            self.embeddings.append(embedding)  # Сохранение эмбеддинга в список

        self.embeddings = np.array(self.embeddings)  # Преобразование списка эмбеддингов в массив NumPy

        # Создание индекса для поиска
        if faiss_index_method == 'IndexFlatL2':
            self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        elif faiss_index_method == 'IndexHNSW':
            self.index = faiss.IndexHNSWFlat(self.embeddings.shape[1], 32)
        else:
            raise ValueError("Unknown FAISS index method")

        self.index.add(self.embeddings)  # Добавление эмбеддингов в индекс

    def retrieve(self, query, top_k=1):
        """
        Поиск наиболее релевантных страниц по запросу пользователя.
        :param query: Запрос пользователя.
        :param top_k: Количество наиболее релевантных результатов для возврата.
        :return: Список текстов наиболее релевантных страниц.
        """
        query_embedding = self.model.encode([query])  # Создание эмбеддинга для запроса
        distances, indices = self.index.search(query_embedding, top_k)  # Поиск по индексу
        results = [self.texts[idx] for idx in indices[0]]  # Извлечение текстов для найденных индексов
        return results  # Возврат найденных текстов

    "(Текстовый файл для проверки, all-MiniLM-L6-v2 проверить либо другую модель, для эмбендингов взять с чат гпт)"