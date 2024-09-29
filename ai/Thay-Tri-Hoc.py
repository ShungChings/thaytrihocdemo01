import os
import json
import difflib
import speech_recognition as sr
from gtts import gTTS
import pygame
from datetime import datetime

# Hàm nhận diện giọng nói
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Nói gì đó...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='vi-VN')
            print(f"Bạn đã nói: {text}")
            return text.lower()  # Trả về chữ thường để dễ so sánh
        except sr.UnknownValueError:
            print("Không nhận diện được giọng nói")
        except sr.RequestError:
            print("Lỗi kết nối với dịch vụ nhận diện giọng nói")
        return None

# Hàm chuyển văn bản thành giọng nói
def text_to_speech(text):
    tts = gTTS(text=text, lang='vi')
    save_path = os.path.join(os.path.expanduser("~"), "Documents", "response.mp3")

    # Xóa tệp nếu đã tồn tại
    if os.path.exists(save_path):
        os.remove(save_path)

    tts.save(save_path)
    pygame.mixer.init()
    pygame.mixer.music.load(save_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    # Giải phóng tệp âm thanh
    pygame.mixer.music.unload()

    # Xóa tệp sau khi phát xong
    if os.path.exists(save_path):
        os.remove(save_path)

# Hàm lấy ngày hiện tại
def get_current_date():
    today = datetime.now()
    return today.strftime("%d/%m/%Y")

# Hàm đọc dữ liệu từ file JSON
def load_data_from_json(file_path):
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file '{file_path}'. Vui lòng kiểm tra đường dẫn.")
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data.get('data', [])

# Hàm tìm kiếm câu hỏi gần đúng
def find_best_match(user_input, data):
    questions = [item['question'] for item in data]
    best_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.6)
    
    if best_match:
        for item in data:
            if item['question'] == best_match[0]:
                return item['answer']
    return None

# Hàm kiểm tra câu nói để thoát chương trình
def check_exit_conditions(user_input):
    exit_phrases = ["tạm biệt", "cảm ơn"]  # Các cụm từ thoát chương trình
    for phrase in exit_phrases:
        if phrase in user_input:
            return True
    return False

if __name__ == "__main__":
    # Tải dữ liệu câu hỏi và câu trả lời từ file JSON
    data_file_path = 'data.json'
    data = load_data_from_json(data_file_path)

    if data:
        while True:
            user_input = recognize_speech()
            if user_input:
                # Kiểm tra nếu người dùng nói "tạm biệt" hoặc "cảm ơn"
                if check_exit_conditions(user_input):
                    text_to_speech("Không có gì. Nếu bạn cần giúp gì hãy gọi tôi!")
                    print("Thầy Trí Học 4.0: Không có gì. Nếu bạn cần giúp gì hãy gọi tôi!")
                    break  # Thoát chương trình

                # Xử lý câu hỏi và phản hồi
                response = find_best_match(user_input.lower(), data)

                if response:
                    if "{date}" in response:
                        response = response.replace("{date}", get_current_date())
                else:
                    response = "Xin lỗi, tôi chưa hiểu câu hỏi của bạn."

                print(f"Thầy Trí Học 4.0: {response}")
                text_to_speech(response)
    else:
        print("Không có dữ liệu câu hỏi và câu trả lời.")
