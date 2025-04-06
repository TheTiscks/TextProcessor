from flask import Flask, request, jsonify, send_from_directory
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad      #pycryptodome package
from base64 import b64encode, b64decode
import os

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
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
        // Валидация ключа
            if (!key) throw new Error("Введите ключ");
            if (!/^[A-Za-z0-9+/=]+$/.test(key)) {
                throw new Error("Ключ должен быть в формате Base64");
            }

        // Валидация текста
            if (!text) throw new Error("Введите текст");
            if (mode === 'decrypt' && !/^[A-Za-z0-9+/=]+$/.test(text)) {
                throw new Error("Для дешифровки нужен Base64");
            }
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
            showError(error.message);
            return;
        }
    }
    function showError(msg) {
        document.getElementById('error').innerHTML = msg;
        document.getElementById('error').style.color = 'red';
    }
    function generateKey() {
        fetch('/generate-key')
            .then(res => res.json())
            .then(data => {
                document.getElementById('key').value = data.key;
                document.getElementById('key-info').innerHTML = 
                    `Ключ ${data.bits}-бит (${data.key.length} символов)`;
        });
    }

    function copyKey() {
        navigator.clipboard.writeText(
            document.getElementById('key').value
        );
    }
    </script>
</head>
<body>
    <textarea id="text" rows="5" placeholder="Введите текст..."></textarea><br>
    <input type="text" id="key" placeholder="Ключ (16 символов)" style="width: 200px"><br>
    <button id="modeBtn" onclick="toggleMode()">Шифровать</button>
    <button onclick="processText()">Выполнить</button>
    <div id="output"></div>
    <div id="error" style="margin: 10px 0"></div>
    <div>
    <button onclick="generateKey()">Сгенерировать</button>
    <input type="text" id="key" placeholder="Ключ в Base64">
    <button onclick="copyKey()">📋</button>
    </div>
<div id="key-info"></div>
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

@app.route('/generate-key', methods=['GET'])
def generate_key():
    # Генерация 256-битного ключа (32 байта) для AES-256
    key_bytes = os.urandom(32)
    key_base64 = b64encode(key_bytes).decode('utf-8')
    return jsonify({
        'status': 'success',
        'key': key_base64,
        'bits': 256,
        'description': 'AES-256 совместимый ключ'
    })

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Неверный формат данных"}), 400

    text = data.get('text', '').strip()
    mode = data.get('mode', '')
    key = data.get('key', '').strip()

    # Детальная валидация
    errors = []
    if not text:
        errors.append("Текст не может быть пустым")
    if not key:
        errors.append("Ключ не может быть пустым")
    if mode not in ['encrypt', 'decrypt']:
        errors.append("Неверный режим операции")
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        # Декодирование из Base64
        try:
            decoded_key = b64decode(user_key)
        except:
            raise ValueError("Неверный формат ключа. Используйте Base64")

        # Проверка длины ключа
        if len(decoded_key) not in (16, 24, 32):
            raise ValueError(
                "Некорректная длина ключа. Допустимые размеры: "
                "128 бит (16 символов), 192 бит (24) или 256 бит (32)"
            )
        if mode == 'encrypt':
            processed_text = aes_encrypt(text, decoded_key)
            word_count = count_words(text)
        elif mode == 'decrypt':
            processed_text = aes_decrypt(text, decoded_key)
            word_count = count_words(processed_text)
        else:
            raise ValueError("Неверный режим операции")
        return jsonify({
            'status': 'success',
            'text': processed_text,
            'words': word_count,
            'key_type': f"AES-{len(decoded_key) * 8}"
        })
    except Exception as e:
        app.logger.error(f"Ошибка: {str(e)}")
        return jsonify({
            "error": "Внутренняя ошибка сервера",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
    