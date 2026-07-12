from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Твой Telegram бот и ID админа (замени на свои)
BOT_TOKEN = "8843954886:AAEpfaWLm6sTfmq2T-mShBilX8mInCXs3as"  # Замени на реальный токен
ADMIN_ID = 8559381302    # Замени на твой Telegram ID

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        logging.info(f"Получены данные: {data}")
        
        # Проверяем статус платежа
        if data.get('status') == 'paid':
            # Здесь логика: что делать при успешной оплате
            # Например, отправить уведомление админу
            send_telegram_message(f"✅ Платеж прошел! Сумма: {data.get('amount')}")
            
        return "OK", 200
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return "Error", 400

def send_telegram_message(text):
    # Заглушка для отправки в Telegram
    print(f"Сообщение в Telegram: {text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
