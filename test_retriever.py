import fitz  # PyMuPDF для работы с PDF файлами
import faiss  # FAISS для быстрого поиска по эмбеддингам
import numpy as np  # NumPy для работы с массивами
from sentence_transformers import SentenceTransformer  # SentenceTransformer для создания эмбеддингов текста
from file_retrieval import PDFRetriever

# Укажите путь к вашему PDF файлу
pdf_path = 'pythonBook.pdf'

# Создайте объект PDFRetriever
retriever = PDFRetriever(pdf_path)

# Проверьте создание эмбеддингов и индекса
print("Embedding and index created successfully.")

# Задайте тестовый запрос
query = "Оператор class применяется для определения объектов новых типов"
top_k = 3  # Количество наиболее релевантных результатов

# Выполните поиск по запросу
results = retriever.retrieve(query, top_k)

# Выведите результаты
print("Top {} results:".format(top_k))
for idx, result in enumerate(results):
    print("Result {}: {}".format(idx + 1, result))
    print("//////////////////////////////////////////////")