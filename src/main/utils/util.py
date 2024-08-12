import re


def refine(text):
    # 특수 문자 제거
    text = re.sub(r'[^가-힣0-9\s]', '', text)
    # 불필요한 공백 제거
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def save_to_file(text_array):
    if text_array:
        with open("dataset/train_data_output.txt", "w", encoding="utf-8") as file:
            for line in text_array:
                file.write(line + "\n")
