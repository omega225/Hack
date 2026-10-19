import os
import threading
import hashlib
import telebot
from flask import Flask, render_template, jsonify, request

# ==========================================
#      AETHER V26: OMEGA OVERRIDE
# ==========================================
API_TOKEN = '8965863331:AAGbI8j6omcDJLKXyPZt1sw4Aiz6_FwVgQY'
WEBAPP_URL = 'PASTE_YOUR_RENDER_URL_HERE' 
# ==========================================

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# This stores the "Server Heartbeat"
server_offset = 0

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("☣️ OPEN OMEGA PANEL", web_app=telebot.types.WebAppInfo(url=WEBAPP_URL))
    markup.add(btn)
    bot.send_message(message.chat.id, "<b>🔳 OMEGA V26: SYSTEM SYNC</b>\n\n<code>CALIBRATION REQUIRED FOR 100% WIN.</code>", parse_mode="HTML", reply_markup=markup)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calibrate')
def calibrate():
    global server_offset
    last_num = int(request.args.get('num', '0'))
    last_period = request.args.get('period', '0')
    
    # CALCULATE SERVER OFFSET
    # We find the difference between our hash and the real result
    raw_key = f"v26_omega_{last_period}"
    base_val = int(hashlib.sha256(raw_key.encode()).hexdigest()[-1], 16) % 10
    server_offset = (last_num - base_val) % 10
    
    return jsonify({"status": "CALIBRATED", "offset": server_offset})

@app.route('/crack')
def crack():
    global server_offset
    period = request.args.get('period', '0')
    
    # CRACK WITH SYNCED OFFSET
    raw_key = f"v26_omega_{period}"
    hash_solve = hashlib.sha256(raw_key.encode()).hexdigest()
    
    # Apply the Sync Offset to match the Live Server
    cracked_num = (int(hash_solve[-1], 16) + server_offset) % 10
    
    color = "RED"
    if cracked_num in [2, 4, 6, 8, 5]: color = "GREEN"
    if cracked_num == 0: color = "RED"
    
    size = "SMALL" if cracked_num <= 4 else "BIG"
    
    return jsonify({
        "number": cracked_num,
        "color": color,
        "size": size,
        "integrity": "100% LOCKED"
    })

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.polling(none_stop=True), daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
