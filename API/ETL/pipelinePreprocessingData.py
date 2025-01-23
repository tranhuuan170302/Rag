import re
from sklearn.feature_extraction.text import TfidfVectorizer

from settings.settings import file_stopword
# loại bỏ các ký tự đặc biệt
# loại bỏ các chữ số
def remove_numbers_and_special_chars(text):
    """
    Hàm loại bỏ số và các ký tự đặc biệt, giữ lại chữ cái có dấu trong văn bản tiếng Việt.
    """
    # Sử dụng regex để loại bỏ số và ký tự đặc biệt nhưng giữ lại dấu tiếng Việt
    text = re.sub(r'[0-9]', '', text)  # Loại bỏ số
    text = re.sub(r'[^\w\sÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơ'
                  r'ẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪ'
                  r'ỬỮỰỲỴÝỶỸỳỵýỷỹ]', '', text)  # Loại bỏ ký tự đặc biệt nhưng giữ lại dấu tiếng Việt
    text = re.sub(r'\s+', ' ', text)  # Loại bỏ khoảng trắng thừa

    return text.strip()

def load_stopwords(file_path = file_stopword):
    """
    Đọc stopwords từ file và trả về dưới dạng một danh sách.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        stopwords = [line.strip() for line in file]
    return stopwords


def clean_text(text: str, stopwords: list):
    """
    Xử lý văn bản tiếng Việt: Loại bỏ các ký tự không mong muốn và stopwords dạng từ đơn hoặc cụm từ.
    """
    # Loại bỏ các ký tự đặc biệt nhưng giữ lại dấu tiếng Việt
    text = re.sub(r'[^\w\s]', '', text)

    # Đưa về chữ thường
    text = text.lower()

    # Loại bỏ stopwords
    for stopword in stopwords:
        # Sử dụng re.sub để loại bỏ stopword (dạng từ hoặc cụm từ) khỏi văn bản
        pattern = r'\b' + re.escape(stopword) + r'\b'
        text = re.sub(pattern, '', text)

    # Loại bỏ khoảng trắng thừa do việc loại bỏ stopwords
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def calculate_tfidf(corpus):
    """
    Tính toán TF-IDF cho một tập các văn bản (corpus) và trả về các từ quan trọng.
    """
    # Khởi tạo vectorizer với giá trị TF-IDF
    vectorizer = TfidfVectorizer()

    # Tính toán TF-IDF cho toàn bộ corpus
    X = vectorizer.fit_transform(corpus)

    # Lấy ra các từ tương ứng với các cột trong ma trận TF-IDF
    feature_names = vectorizer.get_feature_names_out()

    # Trả về ma trận TF-IDF và danh sách các từ
    return X, feature_names

def filter_important_words(texts, X, feature_names, threshold=0.1):
    """
    Loại bỏ những từ không quan trọng dựa trên giá trị TF-IDF (threshold là ngưỡng để loại bỏ từ).
    Trả về văn bản hoàn chỉnh sau khi lọc từ không quan trọng.
    """
    important_texts = []
    
    for doc_index, text in enumerate(texts):
        # Tách từ trong văn bản
        words = text.split()

        # Lấy ra các giá trị TF-IDF tương ứng của văn bản hiện tại
        doc_tfidf = X[doc_index].toarray().flatten()

        # Giữ lại những từ có giá trị TF-IDF cao hơn threshold
        important_words = [
            word for word in words if word in feature_names and doc_tfidf[feature_names.tolist().index(word)] > threshold
        ]

        # Ghép lại các từ thành văn bản hoàn chỉnh
        important_texts.append(" ".join(important_words))

    return important_texts

def pipeline_processing(text, stopword, threshold=0.1):
    
    # lượt bỏ số và dấu 
    text = remove_numbers_and_special_chars(text)
    
    # xử lý văn bản
    clean_texts = clean_text(text, stopword)
    
    return clean_texts