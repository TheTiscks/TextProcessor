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

@app.route('/')
def home():
    return HTML

@app.route('/process', methods=['POST'])
def process():
    text = request.json.get('text', '')
    
    if not text.strip():
        return jsonify({'error': 'Введите текст для анализа'}), 400
    
    try:
        # Убираем shlex.quote и передаем текст напрямую
        count_result = subprocess.run(
            ['java', '-cp', '.', 'TextEncryptor', 'count', text],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        words = count_result.stdout.strip()

        encrypt_result = subprocess.run(
            ['java', '-cp', '.', 'TextEncryptor', 'encrypt', text],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        encrypted = encrypt_result.stdout.strip()

    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': f"Java Error: {e.stderr}"  # Убрали .decode()
        }), 500
        
    except Exception as e:
        return jsonify({
            'error': f"Ошибка: {str(e)}"
        }), 500
    
    return jsonify({
        'words': words,
        'encrypted': encrypted
    })

if __name__ == '__main__':
    app.run(debug=True)
    