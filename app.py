from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

app = Flask(__name__)

# HTML-шаблон с улучшенным интерфейсом
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AES Cryptor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; padding: 20px; }
        .container { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
        input, textarea { width: 100%; margin: 5px 0; padding: 8px; }
        button { background: #4CAF50; color: white; border: none; padding: 10px 20px; cursor: pointer; }
        button:hover { background: #45a049; }
        .switch { display: flex; gap: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>AES Encryptor/Decryptor</h2>
        <div class="switch">
            <button onclick="setMode('encrypt')" id="encryptBtn">Шифрование</button>
            <button onclick="setMode('decrypt')" id="decryptBtn">Дешифровка</button>
        </div>

        <textarea id="text" rows="5" placeholder="Введите текст..."></textarea>
        <input type="password" id="key" placeholder="Ключ (16/24/32 символа)">
        <button onclick="process()" id="actionBtn">Шифровать</button>
        <div id="result" style="margin-top: 10px; word-break: break-all;"></div>
    </div>

    <script>
        let currentMode = 'encrypt';

        function setMode(mode) {
            currentMode = mode;
            document.getElementById('actionBtn').textContent = 
                mode === 'encrypt' ? 'Шифровать' : 'Дешифровать';
            document.querySelectorAll('.switch button').forEach(btn => 
                btn.style.background = btn.id === mode + 'Btn' ? '#45a049' : '#4CAF50');
        }

        async function process() {
            const text = document.getElementById('text').value;
            const key = document.getElementById('key').value;
            const resultDiv = document.getElementById('result');

            resultDiv.innerHTML = 'Обработка...';
            resultDiv.style.color = 'black';

            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        text: text,
                        key: key,
                        mode: currentMode
                    })
                });

                const data = await response.json();

                if (data.error) {
                    resultDiv.style.color = 'red';
                    resultDiv.innerHTML = 'Ошибка: ' + data.error;
                } else {
                    resultDiv.style.color = 'green';
                    resultDiv.innerHTML = `Результат:<br>${data.result}`;
                }
            } catch (e) {
                resultDiv.style.color = 'red';
                resultDiv.innerHTML = 'Ошибка сети: ' + e.message;
            }
        }
    </script>
</body>
</html>
'''


def encrypt_aes(plaintext, key):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(iv + ct_bytes).decode()


def decrypt_aes(ciphertext, key):
    data = base64.b64decode(ciphertext)
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()


@app.route('/')
def home():
    return HTML


@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        text = data['text']
        key = data['key'].encode()
        mode = data['mode']

        # Валидация ключа
        if len(key) not in (16, 24, 32):
            return jsonify({'error': 'Некорректная длина ключа (16/24/32 символа)'}), 400

        # Обработка операции
        if mode == 'encrypt':
            result = encrypt_aes(text, key)
        elif mode == 'decrypt':
            result = decrypt_aes(text, key)
        else:
            return jsonify({'error': 'Неверный режим операции'}), 400

        return jsonify({'result': result})

    except ValueError as e:
        return jsonify({'error': f'Ошибка обработки: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Неизвестная ошибка: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)