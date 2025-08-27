# app.py — минимальная версия без email, без requests
from flask import Flask, request, jsonify, render_template_string, url_for
from datetime import datetime, timedelta
import secrets
import json
import urllib.request
import urllib.error

app = Flask(__name__)
messages_db = {}

# HTML-шаблон: убран input для email, оставлен webhook
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Secure Cryptor (minimal)</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; max-width:800px; margin:2rem auto; }
    textarea,input,select { width:100%; padding:0.7rem; margin-top:0.6rem; border-radius:8px; }
    button { padding:0.8rem 1.2rem; border-radius:8px; cursor:pointer; margin-right:8px; }
    .result { margin-top:1rem; padding:1rem; border-radius:8px; background:#f3f3f3; word-break:break-word; }
  </style>
</head>
<body>
<div>
  <h2>🔒 Secure Cryptor (minimal)</h2>

  <div>
    <button id="encryptBtn" onclick="setMode('encrypt')">🗝️ Шифровать</button>
    <button id="decryptBtn" onclick="setMode('decrypt')">🔓 Дешифровать</button>
  </div>

  <textarea id="text" rows="6" placeholder="Введите текст..."></textarea>
  <input id="key" type="password" placeholder="Ключ (любая длина)"/>
  <input id="notifyWebhook" type="url" placeholder="Webhook URL (опционально)" />

  <div id="lifetimeSection" style="margin-top:0.6rem;">
    <select id="lifetime">
      <option value="hour">1 час</option>
      <option value="day" selected>1 день</option>
      <option value="week">1 неделя</option>
    </select>
  </div>

  <div style="margin-top:0.8rem;">
    <button onclick="process()" id="actionBtn">Шифровать</button>
    <button onclick="createSecretLink()">Создать ссылку</button>
  </div>

  <div id="result" class="result"></div>
  <div id="linkResult" class="result" style="display:none;"></div>
</div>

<script>
let currentMode = 'encrypt';
function setMode(mode){
  currentMode = mode;
  document.getElementById('actionBtn').textContent = mode === 'encrypt' ? 'Шифровать' : 'Дешифровать';
  document.getElementById('lifetimeSection').style.display = mode === 'encrypt' ? 'block' : 'none';
  document.getElementById('encryptBtn').style.opacity = mode === 'encrypt' ? 1 : 0.7;
  document.getElementById('decryptBtn').style.opacity = mode === 'decrypt' ? 1 : 0.7;
}
setMode('encrypt');

function showError(msg){
  const r = document.getElementById('result');
  r.style.color = '#c62828'; r.textContent = msg;
}
function showSuccess(msg){
  const r = document.getElementById('result');
  r.style.color = '#2e7d32'; r.textContent = msg;
}

async function process(){
  const text = document.getElementById('text').value;
  const key = document.getElementById('key').value;
  if(!text || !key){ showError('Заполните текст и ключ'); return; }
  try{
    if(currentMode === 'encrypt'){
      const encrypted = CryptoJS.AES.encrypt(text, key).toString();
      showSuccess('Зашифровано: ' + encrypted);
    } else {
      const bytes = CryptoJS.AES.decrypt(text, key);
      const decrypted = bytes.toString(CryptoJS.enc.Utf8);
      if(!decrypted) throw new Error('bad');
      showSuccess('Дешифровано: ' + decrypted);
    }
  } catch(e){
    showError('Ошибка шифрования/дешифрования. Проверьте ключ и данные.');
  }
}

async function createSecretLink(){
  const text = document.getElementById('text').value;
  const key = document.getElementById('key').value;
  const lifetime = document.getElementById('lifetime').value;
  const notifyWebhook = document.getElementById('notifyWebhook').value || null;

  if(!text || !key){ showError('Заполните текст и ключ'); return; }

  try{
    const encrypted = CryptoJS.AES.encrypt(text, key).toString();
    const res = await fetch('/create', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        encrypted_msg: encrypted,
        lifetime: lifetime,
        notify_webhook: notifyWebhook
      })
    });
    const data = await res.json();
    if(data.url){
      const lr = document.getElementById('linkResult');
      lr.style.display = 'block';
      lr.innerHTML = '<strong>Ссылка:</strong><br><a href="'+data.url+'" target="_blank">'+data.url+'</a>';
    } else {
      showError('Не удалось создать ссылку');
    }
  } catch(e){
    console.error(e);
    showError('Ошибка при создании ссылки');
  }
}
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route('/create', methods=['POST'])
def create_message():
    data = request.get_json(force=True) or {}
    encrypted = data.get('encrypted_msg')
    lifetime_key = data.get('lifetime', 'day')
    notify_webhook = data.get('notify_webhook')

    if not encrypted:
        return jsonify({'error': 'encrypted_msg required'}), 400

    lifetimes = {
        'hour': timedelta(hours=1),
        'day': timedelta(days=1),
        'week': timedelta(weeks=1)
    }
    lifetime = lifetimes.get(lifetime_key, timedelta(days=1))

    msg_id = secrets.token_urlsafe(16)
    messages_db[msg_id] = {
        'encrypted': encrypted,
        'expires': datetime.utcnow() + lifetime,
        'views_left': 1,
        'notify_webhook': notify_webhook
    }

    url = url_for('view_message', msg_id=msg_id, _external=True)
    return jsonify({'url': url})


@app.route('/m/<msg_id>')
def view_message(msg_id):
    entry = messages_db.get(msg_id)
    now = datetime.utcnow()
    if not entry or now > entry['expires']:
        messages_db.pop(msg_id, None)
        return '''
        <div style="max-width:600px;margin:3rem auto;padding:2rem;text-align:center;">
          <h2 style="color:#c62828">Сообщение устарело</h2>
          <p>Это сообщение было автоматически удалено или не найдено.</p>
        </div>
        '''

    encrypted_json = json.dumps(entry['encrypted'])
    page = f'''
    <!doctype html><html><head><meta charset="utf-8"><title>Secret</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    </head><body>
      <div style="max-width:700px;margin:3rem auto;padding:2rem;border-radius:8px;background:#fff;">
        <h2>🔒 Секретное сообщение</h2>
        <div id="content"></div>
        <script>
          const encrypted = {encrypted_json};
          const key = prompt('Введите ключ для расшифровки:');
          try {{
            const bytes = CryptoJS.AES.decrypt(encrypted, key);
            const text = bytes.toString(CryptoJS.enc.Utf8);
            if(text){{
              document.getElementById('content').innerHTML = '<div style="color:#2e7d32;font-size:1.05rem;white-space:pre-wrap;">' + text + '</div><p style="color:#666">Сообщение больше не доступно.</p>';
              fetch('/consume/{msg_id}').catch(()=>{});
            }} else {{
              throw new Error('bad key');
            }}
          }} catch(e) {{
            document.getElementById('content').innerHTML = '<div style="color:#c62828;">Неверный ключ или сообщение повреждено</div>';
          }}
        </script>
      </div>
    </body></html>
    '''
    return page


def send_notification(msg_id):
    """Отправка webhook-уведомления (если указан webhook)."""
    entry = messages_db.get(msg_id)
    if not entry:
        return

    webhook = entry.get('notify_webhook')
    if not webhook:
        return

    payload = json.dumps({'event': 'message_viewed', 'msg_id': msg_id}).encode('utf-8')
    req = urllib.request.Request(webhook, data=payload, headers={'Content-Type': 'application/json'})
    try:
        # timeout короткий, чтобы не блокировать сильно сервер
        with urllib.request.urlopen(req, timeout=5) as resp:
            # игнорируем содержимое, логируем только код при необходимости
            pass
    except urllib.error.URLError as e:
        app.logger.debug(f"Webhook POST error for {msg_id}: {e}")


@app.route('/consume/<msg_id>')
def consume_message(msg_id):
    entry = messages_db.get(msg_id)
    if not entry:
        return '', 204
    try:
        entry['views_left'] = max(0, entry.get('views_left', 1) - 1)
        if entry['views_left'] <= 0:
            try:
                send_notification(msg_id)
            finally:
                messages_db.pop(msg_id, None)
    except Exception as e:
        app.logger.error(f"Consume error: {e}")
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
