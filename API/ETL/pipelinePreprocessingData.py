import re
from API.settings.settings import file_stopword

def remove_numbers_and_special_chars(text):
    """
    The function is remove the special character, but not remove the VietNamese character
    input:
        text: just text
    output:
        text: is clean
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

def pipeline_processing(text, stopword, threshold=0.1):

    text = remove_numbers_and_special_chars(text)
    clean_texts = clean_text(text, stopword)
    
    return clean_texts
