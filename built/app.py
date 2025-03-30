from flask import Flask, request, jsonify, send_from_directory
import subprocess

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Текстовый процессор</title>
    <script>
    async function processText() {
        const text = document.getElementById('text').value;
        const response = await fetch('/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const result = await response.json();
        document.getElementById('output').innerHTML = `
            Слов: ${result.words}<br>
            Зашифровано: ${result.encrypted}
        `;
    }
    </script>
</head>
<body>
    <textarea id="text" rows="5"></textarea><br>
    <button onclick="processText()">Анализ</button>
    <div id="output"></div>
</body>
</html>
'''


@app.route('/')
def home():
    return HTML

@app.route('/process', methods=['POST'])
def process():
    text = request.json['text']
    
    # Вызов C-программы для подсчета слов
    c_result = subprocess.run(
        ['./text_stats.exe'], 
        input=text.encode(), 
        capture_output=True
    )
    words = c_result.stdout.decode().strip()
    
    # Вызов Java-программы для шифрования
    java_result = subprocess.run(
        ['java', 'TextEncryptor', text], 
        capture_output=True
    )
    encrypted = java_result.stdout.decode().strip()
    
    return jsonify({
        'words': words,
        'encrypted': encrypted
    })

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
    app.run(debug=True)