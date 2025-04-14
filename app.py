from flask import Flask, request, jsonify, send_from_directory, url_for
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import secrets
import requests
import os
import smtplib


app = Flask(__name__)
messages_db = {}

SMTP_CONFIG = {
    'server': 'smtp.elasticemail.com',
    'port': 2525,
    'username': 'tiscks@mail.ru',
    'password': '',
    'from_email': 'noreply@tisckstext.com'
} # config for SMTP
# not wirking atm

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Secure Cryptor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <style>
        body { 
            font-family: 'Arial', sans-serif; 
            max-width: 700px; 
            margin: 2rem auto; 
            padding: 0 1rem;
            background: #f0f2f5;
        }
        .container { 
            background: white; 
            border-radius: 12px; 
            padding: 2rem; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }
        h2 { 
            color: #2d3436; 
            margin: 0 0 2rem 0; 
            font-size: 1.8rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        textarea, input, select {
            width: 95%;
            margin: 0.8rem 0;
            padding: 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        textarea:focus, input:focus, select:focus {
            border-color: #4CAF50;
            outline: none;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        button:hover { 
            background: #45a049; 
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }
        .button-group {
            display: flex;
            gap: 1rem;
            margin: 1.5rem 0;
        }
        #linkBtn {
            background: #2196F3;
        }
        #linkBtn:hover {
            background: #1976D2;
        }
        .result-box {
            margin: 1.5rem 0;
            padding: 1.5rem;
            border-radius: 8px;
            word-break: break-all;
        }
        .success {
            background: #e8f5e9;
            border: 2px solid #c8e6c9;
            color: #2e7d32;
        }
        .error {
            background: #ffebee;
            border: 2px solid #ffcdd2;
            color: #c62828;
        }
        .link-result {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 2px solid #eee;
        }
        .lifetime-selector {
            margin: 1rem 0;
            display: none;
        }
        select {
            background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'><path fill='%23666' d='M7 10l5 5 5-5z'/></svg>") no-repeat right 1rem center/15px;
            -webkit-appearance: none;
            -moz-appearance: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔒 Secure Cryptor</h2>

        <div class="button-group">
            <button onclick="setMode('encrypt')" id="encryptBtn">🗝️ Шифровать</button>
            <button onclick="setMode('decrypt')" id="decryptBtn">🔓 Дешифровать</button>
        </div>

        <textarea id="text" rows="5" placeholder="✏️ Введите текст..."></textarea>
        <input type="password" id="key" placeholder="🔑 Ключ (любая длина)">
        <input type="email" id="notifyEmail" placeholder="📧 Email для уведомления (опционально)">
        <input type="url" id="notifyWebhook" placeholder="🌐 Webhook URL (опционально)">

        <div class="lifetime-selector" id="lifetimeSection">
            <select id="lifetime">
                <option value="hour">⏳ 1 час</option>
                <option value="day">⏳ 1 день</option>
                <option value="week">⏳ 1 неделя</option>
            </select>
        </div>

        <div class="button-group">
            <button onclick="process()" id="actionBtn">🚀 Выполнить</button>
            <button onclick="createSecretLink()" id="linkBtn">🌐 Создать ссылку</button>
        </div>

        <div id="result" class="result-box"></div>
        <div id="linkResult" class="result-box link-result"></div>
    </div>

    <script>
        let currentMode = 'encrypt';

        function setMode(mode) {
            currentMode = mode;
            const encryptBtn = document.getElementById('encryptBtn');
            const decryptBtn = document.getElementById('decryptBtn');

            // Обновление кнопок режима
            [encryptBtn, decryptBtn].forEach(btn => 
                btn.style.background = btn.id === `${mode}Btn` ? '#45a049' : '#4CAF50');

            // Обновление основной кнопки
            document.getElementById('actionBtn').innerHTML = 
                mode === 'encrypt' ? '🚀 Шифровать' : '🚀 Дешифровать';

            // Показ/скрытие выбора времени жизни
            document.getElementById('lifetimeSection').style.display = 
                mode === 'encrypt' ? 'block' : 'none';
        }

        async function process() {
            const text = document.getElementById('text').value;
            const key = document.getElementById('key').value;
            const resultDiv = document.getElementById('result');

            resultDiv.className = '';
            resultDiv.innerHTML = '';

            if (!text || !key) {
                showError('❗ Заполните все поля!');
                return;
            }

            try {
                let result;
                if (currentMode === 'encrypt') {
                    result = CryptoJS.AES.encrypt(text, key).toString();
                    resultDiv.innerHTML = `
                        <div class="success">
                            <strong>🔐 Зашифровано:</strong><br>
                            ${result}
                        </div>
                    `;
                } else {
                    const bytes = CryptoJS.AES.decrypt(text, key);
                    result = bytes.toString(CryptoJS.enc.Utf8);
                    if (!result) throw new Error();
                    resultDiv.innerHTML = `
                        <div class="success">
                            <strong>🎉 Дешифровано:</strong><br>
                            ${result}
                        </div>
                    `;
                }
            } catch (e) {
                showError('❌ Ошибка: Неверный ключ или данные');
            }
        }

        async function createSecretLink() {
            const text = document.getElementById('text').value;
            const key = document.getElementById('key').value;
            const lifetime = document.getElementById('lifetime').value;
            const linkResult = document.getElementById('linkResult');
            const notifyEmail = document.getElementById('notifyEmail').value;
            const notifyWebhook = document.getElementById('notifyWebhook').value;
            
            if (!text || !key) {
                showError('❗ Заполните текст и ключ!');
                return;
            }

            try {
                const encrypted = CryptoJS.AES.encrypt(text, key).toString();
                const response = await fetch('/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        encrypted_msg: encrypted,
                        lifetime: lifetime,
                        notify_email: notifyEmail,  // Новые поля
                        notify_webhook: notifyWebhook
                    })
                });

                const data = await response.json();
                if (data.url) {
                    linkResult.innerHTML = `
                        <div class="success">
                            <strong>🔗 Ссылка:</strong><br>
                            <a href="${data.url}" target="_blank">${data.url}</a>
                            <p style="margin-top: 0.5rem; font-size: 0.9em; color: #666;">
                                Сообщение самоуничтожится через ${document.getElementById('lifetime').options[document.getElementById('lifetime').selectedIndex].text}
                            </p>
                        </div>
                    `;
                }
            } catch (e) {
                showError('❌ Ошибка при создании ссылки');
            }
        }

        function showError(msg) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<div class="error">${msg}</div>`;
        }
    </script>
</body>
</html>
'''


@app.route('/create', methods=['POST'])
def create_message():
    data = request.json
    msg_id = secrets.token_urlsafe(16)
    lifetimes = {
        'hour': timedelta(hours=1),
        'day': timedelta(days=1),
        'week': timedelta(weeks=1)
    }
    messages_db[msg_id] = {
        'encrypted': data['encrypted_msg'],
        'expires': datetime.now() + lifetimes[data['lifetime']],
        'views_left': 1,
        'notify_email': data.get('notify_email'),
        'notify_webhook': data.get('notify_webhook')
    }
    return jsonify({'url': f'http://localhost:5000/m/{msg_id}'})


@app.route('/m/<msg_id>')
def view_message(msg_id):
    entry = messages_db.get(msg_id)
    if not entry or datetime.now() > entry['expires']:
        if msg_id in messages_db: del messages_db[msg_id]
        return '''
            <div style="max-width: 600px; margin: 4rem auto; padding: 2rem; text-align: center;">
                <h2 style="color: #c62828;">⏳ Сообщение устарело</h2>
                <p>Это сообщение было автоматически удалено</p>
            </div>
        '''
    return f'''
        <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
        <div style="max-width: 600px; margin: 4rem auto; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="margin-bottom: 1.5rem;">🔒 Секретное сообщение</h2>
            <div id="content" style="padding: 1.5rem; background: #f8f9fa; border-radius: 8px;"></div>
            <script>
                const encrypted = "{entry['encrypted']}";
                const key = prompt('🔑 Введите ключ для расшифровки:');
                try {{
                    const bytes = CryptoJS.AES.decrypt(encrypted, key);
                    const text = bytes.toString(CryptoJS.enc.Utf8);
                    if (text) {{
                        document.getElementById('content').innerHTML = `
                            <div style="color: #2e7d32; font-size: 1.1rem;">${{text}}</div>
                            <p style="color: #666; margin-top: 1rem;">✋ Это сообщение больше не доступно</p>
                        `;
                        fetch('/consume/{msg_id}');
                    }} else {{
                        throw new Error();
                    }}
                }} catch (e) {{
                    document.getElementById('content').innerHTML = 
                        '<div style="color: #c62828;">❌ Неверный ключ или сообщение повреждено</div>';
                }}
            </script>
        </div>
    '''


def send_notification(msg_id):
    entry = messages_db.get(msg_id)
    if not entry:
        return
    # Email уведомление
    if entry.get('notify_email'):
        try:
            print(f"[DEBUG] Попытка отправки email на {entry['notify_email']}")
            msg = MIMEText(f"Сообщение {url_for('view_message', msg_id=msg_id, _external=True)} было просмотрено")
            msg['Subject'] = 'SecureCryptor: Сообщение просмотрено'
            msg['From'] = SMTP_CONFIG['from_email']
            msg['To'] = entry['notify_email']
            with smtplib.SMTP(SMTP_CONFIG['server'], SMTP_CONFIG['port']) as server:
                server.starttls()  # Обязательно для порта 2525
                server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
                print("[DEBUG] Email отправлен успешно!")
        except Exception as e:
            print(f"[ERROR] Ошибка отправки email: {str(e)}")
    # Webhook уведомление
    if entry.get('notify_webhook'):
        try:
            requests.post(
                entry['notify_webhook'],
                json={'event': 'message_viewed', 'msg_id': msg_id},
                timeout=5
            )
        except Exception as e:
            print(f"Ошибка webhook: {e}")

@app.route('/consume/<msg_id>')
def consume_message(msg_id):
    if msg_id in messages_db:
        try:
            if messages_db[msg_id]['views_left'] <= 1:
                send_notification(msg_id)
        except Exception as e:
            print(f"Notification error: {e}")
        finally:
            del messages_db[msg_id]
    return '', 200


@app.route('/')
def home():
    return HTML


if __name__ == '__main__':
    app.run(debug=True)
    
