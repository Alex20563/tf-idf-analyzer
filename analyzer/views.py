from django.shortcuts import render
import math
import re
from docx import Document

def extract_text_from_docx(file):
    """Считывает текст из Word-документа (.docx)"""
    doc = Document(file)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

def process_text(text):
    """
    Обработка текста:
    - Захватывает английские и русские слова
    - Подсчитывает TF
    - Вычисляет IDF
    """
    words = re.findall(r"[а-яёА-ЯЁa-zA-Z]+(?:'[a-z]+)?", text.lower(), re.IGNORECASE | re.UNICODE)
    total_words = len(words)

    freq = {}
    for word in words:
        word = word.lower()
        freq[word] = freq.get(word, 0) + 1

    tf_idf_data = []
    for word, count in freq.items():
        tf = count
        idf = math.log(total_words / (1 + count))
        tf_idf_data.append((word, tf, idf))

    tf_idf_data.sort(key=lambda x: x[2], reverse=True)
    return tf_idf_data[:50]


def index(request):
    """
    Главная view-функция:
    - Обрабатывает POST-запрос с загруженным файлом
    - Проверяет расширение
    - Считывает содержимое файла (txt или docx)
    - Отдаёт шаблону таблицу с результатами
    """
    context = {}

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name.lower()

        try:
            if filename.endswith('.txt'):
                text = uploaded_file.read().decode('utf-8')
            elif filename.endswith('.docx'):
                text = extract_text_from_docx(uploaded_file)
            else:
                context['error'] = 'Поддерживаются только .txt и .docx файлы.'
                return render(request, 'analyzer/index.html', context)

            # Обработка текста и формирование результата
            context['data'] = process_text(text)
        except Exception as e:
            context['error'] = f'Ошибка при обработке файла: {e}'

    return render(request, 'analyzer/index.html', context)
