from flask import Flask, request, jsonify
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
        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            
            if (!response.ok) {
                throw new Error('Сервер вернул ошибку');
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

@app.route('/')
def home():
    return HTML

@app.route('/process', methods=['POST'])
def process():
    text = request.json.get('text', '')
    
    if not text:
        return jsonify({
            'error': 'Введите текст для анализа'
        }), 400
    
    try:
        # Вызов C-программы
        print(f"[DEBUG] C-ввод: '{text}'")
        c_result = subprocess.run(
            ['./text_stats.exe'],
            input=text,
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        words = c_result.stdout.strip()
        print(f"[DEBUG] C-результат: {words}")
        
        # Вызов Java-программы
        print(f"[DEBUG] Java-ввод: '{text}'")
        java_result = subprocess.run(
            ['java', 'TextEncryptor', text],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        encrypted = java_result.stdout.strip()
        print(f"[DEBUG] Java-результат: {encrypted}")
        
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e.stderr}")
        return jsonify({
            'error': f"Ошибка обработки: {e.stderr}"
        }), 500
        
    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({
            'error': f"Неизвестная ошибка: {str(e)}"
        }), 500
    
    return jsonify({
        'words': words,
        'encrypted': encrypted
    })

if __name__ == '__main__':
    app.run(debug=True)