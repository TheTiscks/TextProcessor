from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

# Временное хранилище сообщений
messages_db = {}

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AES Cryptor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <style>
        /* ... существующие стили ... */
        .lifetime-selector { margin: 10px 0; }
        .link-result { margin-top: 10px; word-break: break-all; }
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
        <input type="password" id="key" placeholder="Ключ (любая длина)">

        <div class="lifetime-selector" id="lifetimeSection" style="display: none;">
            <label>Время жизни:</label>
            <select id="lifetime">
                <option value="hour">1 час</option>
                <option value="day">1 день</option>
                <option value="week">1 неделя</option>
            </select>
        </div>

        <button onclick="process()" id="actionBtn">Шифровать</button>
        <button onclick="createSecretLink()" id="linkBtn">Создать секретную ссылку</button>

        <div id="result"></div>
        <div id="linkResult" class="link-result"></div>
    </div>

    <script>
        let currentMode = 'encrypt';

        function setMode(mode) {
            currentMode = mode;
            const btn = document.getElementById('actionBtn');
            btn.textContent = mode === 'encrypt' ? 'Шифровать' : 'Дешифровать';
            document.querySelectorAll('.switch button').forEach(b => 
                b.style.background = b.id === mode + 'Btn' ? '#45a049' : '#4CAF50');

            // Показываем выбор времени жизни только для шифрования
            document.getElementById('lifetimeSection').style.display = 
                mode === 'encrypt' ? 'block' : 'none';
        }

        async function createSecretLink() {
            const text = document.getElementById('text').value;
            const key = document.getElementById('key').value;
            const lifetime = document.getElementById('lifetime').value;

            if (!text || !key) {
                showError('Заполните текст и ключ!');
                return;
            }

            try {
                // Шифруем сообщение
                const encrypted = CryptoJS.AES.encrypt(text, key).toString();

                // Отправляем на сервер
                const response = await fetch('/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        encrypted_msg: encrypted,
                        lifetime: lifetime
                    })
                });

                const data = await response.json();
                if (data.url) {
                    document.getElementById('linkResult').innerHTML = 
                        `<strong>Ссылка:</strong><br><a href="${data.url}">${data.url}</a>`;
                }
            } catch (e) {
                showError('Ошибка при создании ссылки: ' + e.message);
            }
        }

        /* ... остальные функции process() и showError() ... */
    </script>
</body>
</html>
'''


@app.route('/create', methods=['POST'])
def create_message():
    data = request.json
    msg_id = secrets.token_urlsafe(16)

    # Рассчет времени жизни
    lifetimes = {
        'hour': timedelta(hours=1),
        'day': timedelta(days=1),
        'week': timedelta(weeks=1)
    }

    messages_db[msg_id] = {
        'encrypted': data['encrypted_msg'],
        'expires': datetime.now() + lifetimes[data['lifetime']],
        'views_left': 1
    }

    return jsonify({'url': f'/m/{msg_id}'})


@app.route('/m/<msg_id>')
def view_message(msg_id):
    entry = messages_db.get(msg_id)

    if not entry or datetime.now() > entry['expires']:
        if msg_id in messages_db: del messages_db[msg_id]
        return '''
            <h3>Сообщение не найдено или просрочено</h3>
            <p>Это сообщение было автоматически удалено</p>
        '''

    return f'''
        <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
        <div style="max-width: 600px; margin: 50px auto; padding: 20px;">
            <h3>Секретное сообщение 🔒</h3>
            <div id="content" style="margin: 20px 0; padding: 15px; border: 1px solid #ddd;"></div>
            <script>
                const encrypted = "{entry['encrypted']}";
                const key = prompt('Введите ключ для расшифровки:');

                try {{
                    const bytes = CryptoJS.AES.decrypt(encrypted, key);
                    const text = bytes.toString(CryptoJS.enc.Utf8);
                    if (!text) throw new Error();

                    document.getElementById('content').innerHTML = text;
                    fetch('/consume/{msg_id}');
                }} catch (e) {{
                    document.getElementById('content').innerHTML = 
                        '<p style="color: red">Неверный ключ или сообщение повреждено</p>';
                }}
            </script>
        </div>
    '''


@app.route('/consume/<msg_id>')
def consume_message(msg_id):
    if msg_id in messages_db:
        messages_db[msg_id]['views_left'] -= 1
        if messages_db[msg_id]['views_left'] <= 0:
            del messages_db[msg_id]
    return '', 200


@app.route('/')
def home():
    return HTML


if __name__ == '__main__':
    app.run(debug=True)