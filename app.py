from flask import Flask, request, jsonify, send_from_directory
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import os

app = Flask(__name__)

# Конфигурация AES
SECRET_KEY = os.urandom(16)  # 128-битный ключ
IV = os.urandom(16)          # Вектор инициализации

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Текстовый процессор</title>
    <link rel="icon" href="data:,">
    <script>
    let mode = 'encrypt'; // По умолчанию шифрование

    function toggleMode() {
        mode = mode === 'encrypt' ? 'decrypt' : 'encrypt';
        document.getElementById('modeBtn').textContent = 
            mode === 'encrypt' ? 'Шифровать' : 'Дешифровать';
        document.getElementById('output').innerHTML = '';
    }

    async function processText() {
        const text = document.getElementById('text').value;
        const key = document.getElementById('key').value;
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    text, 
                    key,
                    mode 
                })
            });
            
            const result = await response.json();
            if (!response.ok) throw new Error(result.error);
            
            document.getElementById('output').innerHTML = `
                Режим: ${mode === 'encrypt' ? 'Шифрование' : 'Дешифровка'}<br>
                Результат: ${result.text}
            `;
        } catch (error) {
            document.getElementById('output').innerHTML = 
                'Ошибка: ' + error.message;
        }
    }
    </script>
</head>
<body>
    <textarea id="text" rows="5" placeholder="Введите текст..."></textarea><br>
    <input type="text" id="key" placeholder="Ключ (16 символов)" style="width: 200px"><br>
    <button id="modeBtn" onclick="toggleMode()">Шифровать</button>
    <button onclick="processText()">Выполнить</button>
    <div id="output"></div>
</body>
</html>
'''

def count_words(text: str) -> int:
    return len(text.strip().split()) if text.strip() else 0

def aes_encrypt(text: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC, IV)
    padded_text = pad(text.encode('utf-8'), AES.block_size)
    cipher_text = cipher.encrypt(padded_text)
    return b64encode(cipher_text).decode('utf-8')

def aes_decrypt(cipher_text: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(b64decode(cipher_text))
    return unpad(decrypted, AES.block_size).decode('utf-8')

@app.route('/')
def home():
    return HTML

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '')
    mode = data.get('mode', 'encrypt')
    user_key = data.get('key', '').encode('utf-8')

    try:
        # Валидация ключа
        if len(user_key) != 16:
            raise ValueError("Ключ должен быть 16 байт (16 символов ASCII)")

        if mode == 'encrypt':
            processed = aes_encrypt(text, user_key)
        elif mode == 'decrypt':
            processed = aes_decrypt(text, user_key)
        else:
            raise ValueError("Неверный режим операции")

        return jsonify({
            'text': processed,
            'words': count_words(text if mode == 'encrypt' else processed)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
    