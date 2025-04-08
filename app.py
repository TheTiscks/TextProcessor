from flask import Flask

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AES Cryptor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; padding: 20px; }
        .container { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
        input, textarea { width: 100%; margin: 5px 0; padding: 8px; }
        button { background: #4CAF50; color: white; border: none; padding: 10px 20px; cursor: pointer; }
        button:hover { background: #45a049; }
        .switch { display: flex; gap: 10px; margin: 10px 0; }
        #result { margin-top: 10px; word-break: break-all; }
        .error { color: red; }
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
        <button onclick="process()" id="actionBtn">Шифровать</button>
        <div id="result"></div>
    </div>

    <script>
        let currentMode = 'encrypt';

        function setMode(mode) {
            currentMode = mode;
            const btn = document.getElementById('actionBtn');
            btn.textContent = mode === 'encrypt' ? 'Шифровать' : 'Дешифровать';
            document.querySelectorAll('.switch button').forEach(b => 
                b.style.background = b.id === mode + 'Btn' ? '#45a049' : '#4CAF50');
        }

        function process() {
            const text = document.getElementById('text').value;
            const key = document.getElementById('key').value;
            const resultDiv = document.getElementById('result');

            resultDiv.innerHTML = '';
            resultDiv.className = '';

            if (!text || !key) {
                showError('Заполните все поля!');
                return;
            }

            try {
                let result;
                if (currentMode === 'encrypt') {
                    result = CryptoJS.AES.encrypt(text, key).toString();
                    resultDiv.innerHTML = `<strong>Зашифровано:</strong><br>${result}`;
                } else {
                    const bytes = CryptoJS.AES.decrypt(text, key);
                    result = bytes.toString(CryptoJS.enc.Utf8);
                    if (!result) throw new Error('Неверный ключ или данные');
                    resultDiv.innerHTML = `<strong>Дешифровано:</strong><br>${result}`;
                }
                resultDiv.style.color = 'green';
            } catch (e) {
                showError('Ошибка: ' + e.message);
            }
        }

        function showError(msg) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = msg;
            resultDiv.className = 'error';
        }
    </script>
</body>
</html>
'''


@app.route('/')
def home():
    return HTML


if __name__ == '__main__':
    app.run(debug=True)