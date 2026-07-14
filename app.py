from flask import Flask, request, jsonify
import logging
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Конфигурация
BOT_TOKEN = "8843954886:AAE_s8K-qw2gFn7Z2zQmd9pvt81Cwxya9tA"
ADMIN_ID = 8559381302

# --- ЭНДПОИНТ ДЛЯ UPTIMEROBOT (GET) ---
@app.route('/', methods=['GET'])
def uptime_check():
    """Проверка что сервис жив"""
    return jsonify({
        "status": "ok",
        "service": "RollyPay Webhook Handler",
        "uptime": "alive"
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Альтернативный эндпоинт для health check"""
    return jsonify({
        "status": "healthy",
        "service": "RollyPay Webhook Handler"
    }), 200

# --- ОСНОВНОЙ ВЕБХУК ДЛЯ ROLLYPAY (POST) ---
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        logging.info(f"Получены данные: {data}")
        
        # Проверяем статус платежа
        if data.get('status') == 'paid':
            # Отправляем уведомление админу
            send_telegram_message(f"✅ Платеж прошел! Сумма: {data.get('amount')} {data.get('currency', 'RUB')}")
            
            # Можно также отправить сообщение пользователю через бота
            user_id = extract_user_id(data.get('order_id'))
            if user_id:
                send_telegram_message(f"✅ Пользователь {user_id} оплатил!")
        
        return "OK", 200
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return "Error", 400

def extract_user_id(order_id):
    """Извлекает user_id из order_id"""
    if order_id:
        parts = order_id.split('_')
        if len(parts) > 1:
            return parts[1]  # user_id
    return None

def send_telegram_message(text):
    """Отправка сообщения в Telegram (заглушка - можно заменить на реальную)"""
    # Реальная отправка через Bot API
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": ADMIN_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logging.info("✅ Сообщение отправлено в Telegram")
        else:
            logging.error(f"❌ Ошибка отправки: {response.text}")
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
        print(f"Сообщение (лог): {text}")

if __name__ == '__main__':
    # Запускаем на порту 5000 или из переменной PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
