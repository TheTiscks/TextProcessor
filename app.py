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
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Требуется JSON-тело запроса"}), 400

        text = data.get('text', '')
        mode = data.get('mode', 'encrypt')
        user_key = data.get('key', '')  # Ключ в Base64

        if not user_key:
            return jsonify({"error": "Ключ обязателен"}), 400

        try:
            decoded_key = b64decode(user_key)
        except:
            return jsonify({"error": "Неверный формат ключа (требуется Base64)"}), 400

        # Режим шифрования
        if mode == 'encrypt':
            cipher = AES.new(decoded_key, AES.MODE_CBC, IV)
            padded_text = pad(text.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_text)
            result = b64encode(IV + encrypted).decode('utf-8')

        # Режим дешифровки
        elif mode == 'decrypt':
            encrypted_data = b64decode(text)
            iv = encrypted_data[:16]
            cipher_text = encrypted_data[16:]
            cipher = AES.new(decoded_key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(cipher_text), AES.block_size)
            result = decrypted.decode('utf-8')

        else:
            return jsonify({"error": "Неверный режим (допустимо: encrypt/decrypt)"}), 400

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    