 
  function removeStopWords(input) {
    const stopWords = ["làm sao", "cái gì", "cách nào", "là gì", "tại sao", "như thế nào"];
    let result = input;
    stopWords.forEach(word => {
        const regex = new RegExp(`\\b${word}\\b`, 'gi');
        result = result.replace(regex, '');
    });
    console.log("After removing stop words:", result); // Debugging line
    return result.trim();
}

async function fetchData() {
    const response = await fetch('data.json');
    const data = await response.json();
    return data.data;
}

async function getResponse() {
    let userInput = document.getElementById('user-input').value.toLowerCase();
    console.log("Original input:", userInput); // Debugging line
    userInput = removeStopWords(userInput);
    console.log("Processed input:", userInput); // Debugging line
    let response = "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Hãy thử lại!";
    
    // Lấy dữ liệu từ file JSON
    const data = await fetchData();

    // Cấu hình Fuse.js
    const options = {
        keys: ['question'],
        threshold: 0.3 // Độ nhạy của tìm kiếm
    };
    const fuse = new Fuse(data, options);
    const result = fuse.search(userInput);

    if (result.length > 0) {
        response = result[0].item.answer;
    }

    document.getElementById('response').innerHTML = response;
}