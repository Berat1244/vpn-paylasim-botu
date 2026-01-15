import telebot
from telebot import types
import os, threading, time
from flask import Flask

# --- WEB SUNUCUSU ---
app = Flask('')
@app.route('/')
def home(): return "VPN Botu Aktif!"
def run_flask(): 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))

# --- BOT AYARLARI ---
TOKEN = '8552109076:AAGB_PWP9Tko3UIyDol-8ZQ4xmaP9Omk3m8'
bot = telebot.TeleBot(TOKEN)

# --- MENÜLER ---
def main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📄 Dosya Al", callback_data="cihaz_sec"))
    return markup

def os_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤖 Android", callback_data="setup_android"),
               types.InlineKeyboardButton("🍎 iOS", callback_data="setup_ios"))
    markup.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="main_don"))
    return markup

def android_files():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🟢 Whatsapp Pass (.hc)", callback_data="file_and_wp"),
               types.InlineKeyboardButton("🔴 Youtube Pass (.hc)", callback_data="file_and_yt"))
    markup.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="cihaz_sec"))
    return markup

def ios_files():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🟢 Whatsapp Pass (.npvt)", callback_data="file_ios_wp"),
               types.InlineKeyboardButton("🔴 Youtube Pass (.npvt)", callback_data="file_ios_yt"))
    markup.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="cihaz_sec"))
    return markup

# --- OTOMATİK SİLME FONKSİYONU ---
def auto_delete(chat_id, message_id):
    time.sleep(60) # 60 saniye bekle
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

# --- KOMUTLAR ---
@bot.message_handler(commands=['start'])
def start(m):
    text = "👋 Hoş Geldin!\n\nBu bot ile VPN dosyalarını kolayca alabilirsin ✅\n\nDosya almak için aşağıdaki butonları kullan 🎉"
    bot.send_message(m.chat.id, text, reply_markup=main_menu())

# --- BUTON İŞLEMLERİ ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "main_don":
        bot.edit_message_text("👋 Hoş Geldin!\n\nBu bot ile VPN dosyalarını kolayca alabilirsin ✅", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "cihaz_sec":
        bot.edit_message_text("📱 Cihazınızı seçin:", call.message.chat.id, call.message.message_id, reply_markup=os_menu())
    elif call.data == "setup_android":
        bot.edit_message_text("🤖 Android için dosya seçin:", call.message.chat.id, call.message.message_id, reply_markup=android_files())
    elif call.data == "setup_ios":
        bot.edit_message_text("🍎 iOS için dosya seçin:", call.message.chat.id, call.message.message_id, reply_markup=ios_files())

    elif call.data.startswith("file_"):
        files = {
            "file_and_wp": "Whatsapp.pass.hc",
            "file_and_yt": "Youtube.pass.hc",
            "file_ios_wp": "Whatsapp.pass.npvt",
            "file_ios_yt": "Youtube.pass.npvt"
        }
        file_name = files.get(call.data)
        
        if os.path.exists(file_name):
            bot.answer_callback_query(call.id, "Dosya gönderiliyor...")
            with open(file_name, 'rb') as doc:
                # Dosyayı gönder ve uyarı mesajını ekle
                sent_msg = bot.send_document(
                    call.message.chat.id, 
                    doc, 
                    caption=f"✅ **{file_name}** Hazır!\n\n⚠️ **UYARI: Bu dosya 60 saniye sonra otomatik olarak silinecektir!**",
                    parse_mode="Markdown"
                )
                # Silme işlemini başka bir kolda (thread) başlat
                threading.Thread(target=auto_delete, args=(call.message.chat.id, sent_msg.message_id)).start()
        else:
            bot.answer_callback_query(call.id, "⚠️ Bu dosya şu anda mevcut değil!", show_alert=True)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
