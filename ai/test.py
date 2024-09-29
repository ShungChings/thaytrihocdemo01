import os
import json
import difflib
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox

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
            return "Không nhận diện được giọng nói"
        except sr.RequestError:
            print("Lỗi kết nối với dịch vụ nhận diện giọng nói")
            return "Lỗi kết nối với dịch vụ nhận diện giọng nói"

# Hàm chuyển văn bản thành giọng nói
def text_to_speech(text):
    tts = gTTS(text=text, lang='vi')
    save_path = os.path.join(os.path.expanduser("~"), "Documents", "response.mp3")

    # Xóa tệp nếu đã tồn tại
    if os.path.exists(save_path):
        os.remove(save_path)

    tts.save(save_path)
    
    # Phát âm thanh bằng playsound
    playsound(save_path)

    # Xóa tệp sau khi phát xong
    if os.path.exists(save_path):
        os.remove(save_path)

# Hàm lấy ngày hiện tại
def get_current_date():
    today = datetime.now()
    return today.strftime("%d/%m/%Y")

# Hàm đọc dữ liệu từ file JSON với xử lý lỗi
def load_data_from_json(file_path):
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file '{file_path}'. Vui lòng kiểm tra đường dẫn.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get('data', [])  # Nếu không có key 'data' sẽ trả về một list rỗng
    except json.JSONDecodeError:
        print(f"Lỗi: File '{file_path}' không đúng định dạng JSON.")
        return []
    except Exception as e:
        print(f"Lỗi: Có lỗi khi đọc file '{file_path}': {str(e)}")
        return []

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

# Hàm xử lý chính trong giao diện
def process_speech():
    user_input = recognize_speech()
    
    if user_input:
        # Hiển thị câu nói của người dùng
        user_input_label.config(text=f"Bạn đã nói: {user_input}")
        
        # Kiểm tra nếu người dùng nói "tạm biệt" hoặc "cảm ơn"
        if check_exit_conditions(user_input):
            response = "Không có gì. Nếu bạn cần giúp gì hãy gọi tôi!"
            response_label.config(text=f"Thầy Trí Học 4.0: {response}")
            text_to_speech(response)
            window.quit()  # Thoát chương trình
        else:
            # Xử lý câu hỏi và phản hồi
            response = find_best_match(user_input.lower(), data)
            if response:
                if "{date}" in response:
                    response = response.replace("{date}", get_current_date())
            else:
                response = "Xin lỗi, tôi chưa hiểu câu hỏi của bạn."

            # Hiển thị câu trả lời
            response_label.config(text=f"Thầy Trí Học 4.0: {response}")
            text_to_speech(response)

# Tải dữ liệu câu hỏi và câu trả lời từ file JSON
data_file_path = 'data.json'
data = load_data_from_json(data_file_path)

# Tạo giao diện Tkinter
window = tk.Tk()
window.title("Thầy Trí Học 4.0")

# Tiêu đề
title_label = tk.Label(window, text="Thầy Trí Học 4.0", font=("Arial", 20), pady=10)
title_label.pack()

# Nút để bắt đầu nhận diện giọng nói
start_button = tk.Button(window, text="Bắt đầu nói", font=("Arial", 14), command=process_speech)
start_button.pack(pady=10)

# Nhãn hiển thị câu nói của người dùng
user_input_label = tk.Label(window, text="Bạn đã nói: ", font=("Arial", 14))
user_input_label.pack(pady=10)

# Nhãn hiển thị phản hồi của hệ thống
response_label = tk.Label(window, text="Thầy Trí Học 4.0: ", font=("Arial", 14))
response_label.pack(pady=10)

# Chạy vòng lặp chính của giao diện
window.mainloop()
