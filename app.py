from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Текстовый процессор</title>
    <script>
    async function processText() {
        const text = document.getElementById('text').value;
        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            
            if (!response.ok) {
                throw new Error('Сервер вернул ошибку: ' + (await response.text()));
            }
            
            const result = await response.json();
            document.getElementById('output').innerHTML = `
                Слов: ${result.words}<br>
                Зашифровано: ${result.encrypted}
            `;
        } catch (error) {
            document.getElementById('output').innerHTML = 
                'Ошибка: ' + error.message;
        }
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

def count_words(text: str) -> int:
    """Подсчет слов (аналог Java-функции)"""
    if not text.strip():
        return 0
    return len(text.strip().split())


def encrypt_text(text: str) -> str:
    """Шифрование реверсом (аналог Java-функции)"""
    return text[::-1]


@app.route('/')
def home():
    return HTML

@app.route('/process', methods=['POST'])
def process():
    text = request.json.get('text', '')
    
    if not text.strip():
        return jsonify({'error': 'Введите текст для анализа'}), 400
    
    try:
        words = count_words(text)
        encrypted = encrypt_text(text)
        
        return jsonify({
            'words': words,
            'encrypted': encrypted
        })
        
    except Exception as e:
        return jsonify({
            'error': f"Ошибка обработки: {str(e)}"
        }), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


if __name__ == '__main__':
    app.run(debug=True)
