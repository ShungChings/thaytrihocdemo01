

// Đọc dữ liệu từ file JSON và tạo câu trả lời


async function fetchData() {
    const response = await fetch('data.json');
    const data = await response.json();
    return data.data;
}

async function getResponse() {
    const userInput = document.getElementById('user-input').value.toLowerCase();
    let response = "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Hãy thử lại!";
    
    // Lấy dữ liệu từ file JSON
    const data = await fetchData();

    data.forEach(item => {
        if (userInput.includes(item.question)) {
            response = item.answer;
        }
    });

    document.getElementById('response').innerHTML = response;
}
