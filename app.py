from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

HTML = '''
html page n/a yet
'''


@app.route('/')
def home():
    return HTML

@app.route('/process', methods=['POST'])
def process():
    text = request.json['text']
    
    # Вызов C-программы для подсчета слов
    c_result = subprocess.run(
        ['./text_stats'], 
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

if __name__ == '__main__':
    app.run(debug=True)