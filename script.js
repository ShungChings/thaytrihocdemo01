<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trợ Lý AI Thầy Trí Học 4.0</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #D0EFFF;
        }

        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #FFF;
            border-radius: 10px;
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
        }

        .header {
            text-align: center;
            padding: 20px;
            background-color: #00BFFF;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }

        .chat-box {
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #00BFFF;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
        }

        .message.user {
            background-color: #00BFFF;
            color: white;
            text-align: right;
        }

        .message.bot {
            background-color: #F0F0F0;
            color: #333;
            text-align: left;
        }

        .input-box {
            display: flex;
            justify-content: space-between;
        }

        .input-box input {
            width: 80%;
            padding: 10px;
            border: 1px solid #00BFFF;
            border-radius: 10px;
            outline: none;
        }

        .input-box button {
            width: 18%;
            background-color: #00BFFF;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }

        .input-box button:hover {
            background-color: #008CBA;
        }
    </style>
</head>

<body>

    <div class="chat-container">
        <div class="header">
            Trợ Lý AI - Thầy Trí Học 4.0
        </div>
        <div id="chat-box" class="chat-box">
            <!-- Chat messages will appear here -->
        </div>
        <div class="input-box">
            <input type="text" id="user-input" placeholder="Nhập câu hỏi của bạn...">
            <button onclick="sendMessage()">Gửi</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const userInput = document.getElementById("user-input").value;
            if (userInput.trim() === "") return;

            displayMessage(userInput, "user");
            document.getElementById("user-input").value = "";

            // Gửi tin nhắn của người dùng tới API OpenAI
            const response = await fetch('https://api.openai.com/v1/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer YOUR_API_KEY', // Thay YOUR_API_KEY bằng API key của bạn
                },
                body: JSON.stringify({
                    model: "gpt-3.5-turbo",
                    messages: [{ role: "user", content: userInput }],
                    max_tokens: 150,
                }),
            });

            const data = await response.json();
            const botMessage = data.choices[0].message.content;
            displayMessage(botMessage, "bot");
        }

        function displayMessage(message, type) {
            const chatBox = document.getElementById("chat-box");
            const messageElement = document.createElement("div");
            messageElement.classList.add("message", type);
            messageElement.textContent = message;
            chatBox.appendChild(messageElement);

            // Tự động cuộn xuống cuối cùng của khung chat
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>

</html>
