import scraper
import os
import requests
from twilio.rest import Client

# These will comes from GitHub Secrets (Cloud)
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
TWILIO_FROM = os.environ.get("TWILIO_FROM") # Example: "whatsapp:+14155238886"
MY_NUMBER = os.environ.get("MY_NUMBER")     # Example: "whatsapp:+90555..."

# Telegram Config
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_IDS = os.environ.get("TELEGRAM_CHAT_IDS") # Comma separated

import json
from datetime import datetime

# ... (Previous imports keep same) ...

SUBSCRIBERS_FILE = "subscribers.json"

def send_telegram(message, token, chat_ids):
    if not token or not chat_ids:
        return
    
    # helper to support single ID string or list of IDs string
    if isinstance(chat_ids, list):
         ids = chat_ids
    else:
         ids = [cid.strip() for cid in chat_ids.split(',') if cid.strip()]
         
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    print(f"✈️ Telegram mesajı hazırlanıyor... ({len(ids)} kişi)")
    
    for chat_id in ids:
        try:
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            resp = requests.post(url, json=payload)
            if resp.status_code == 200:
                print(f"✅ Telegram gönderildi: {chat_id}")
            else:
                print(f"❌ Telegram Hata ({chat_id}): {resp.text}")
        except Exception as e:
            print(f"❌ Telegram Hatası: {e}")

def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_subscribers(subs):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(subs, f)

def process_telegram_updates(token):
    if not token: return []
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    subs = load_subscribers()
    original_subs = list(subs)
    
    try:
        resp = requests.get(url).json()
        if "result" not in resp: return subs
        
        # We need to confirm updates to not process them again next time? 
        # Actually with getUpdates default, it returns pending. 
        # Telegram retains messages for 24 hours.
        # To "ack" them, we need to send offset.
        # For simplicity in this ephemeral script, we might process all pending.
        # But if we run daily, we might re-process? 
        # Ideally we store the last update_id. 
        # For a simple "add/remove", idempotent is better.
        # If user says /start 5 times, we just ensure they are in list.
        
        last_update_id = 0
        
        for update in resp["result"]:
            last_update_id = update["update_id"]
            if "message" not in update: continue
            
            chat_id = str(update["message"]["chat"]["id"])
            text = update["message"].get("text", "").lower()
            
            if text in ["/start", "abone", "basla"]:
                if chat_id not in subs:
                    subs.append(chat_id)
                    send_telegram("👋 Hoşgeldiniz! Her sabah 10:00'da menü cebinizde.", token, chat_id)
            
            elif text in ["/stop", "dur", "iptal"]:
                if chat_id in subs:
                    subs.remove(chat_id)
                    send_telegram("🥺 Hoşçakalın! Listeden çıkarıldınız.", token, chat_id)
        
        # Acknowledge updates so we don't process them forever
        if last_update_id > 0:
            requests.get(f"{url}?offset={last_update_id + 1}")
            
    except Exception as e:
        print(f"Update Error: {e}")
        
    if subs != original_subs:
        save_subscribers(subs)
        print(f"💾 Abone listesi güncellendi: {len(subs)} kişi")
        
    return subs

def main():
    # 1. Process New Subscriptions (Always Run)
    current_subs = []
    if TELEGRAM_TOKEN:
        print("📨 Mesajlar kontrol ediliyor... (Saat Başı)")
        current_subs = process_telegram_updates(TELEGRAM_TOKEN)

    # 2. Check Time for Menu Broadcasting (Only at 07:00 UTC = 10:00 TRT)
    # GitHub Actions runner is likely UTC.
    current_hour = datetime.utcnow().hour
    target_hour = 7 # 07:00 UTC = 10:00 TRT

    print(f"⏰ Şu anki saat (UTC): {current_hour}:00. Hedef: {target_hour}:00")

    if current_hour != target_hour:
        print("💤 Menü saati değil. Sadece mesajlar kontrol edildi. Kapanıyor.")
        return

    print("🚀 Saat 10:00! Menü gönderiliyor...")
    print("🍽️ Menü indiriliyor...")
    menu = scraper.get_menu()
    
    if not menu or "Hata" in menu:
        print("❌ Menü alınamadı.")
        return

    # 2. Add Fixed Subscribers (Env Vars)
    fixed_subs = [cid.strip() for cid in (TELEGRAM_CHAT_IDS or "").split(',') if cid.strip()]
    
    # Merge lists (Unique)
    all_telegram_recipients = list(set(current_subs + fixed_subs))
    
    # 3. Send to WhatsApp (Twilio)
    if all([TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, MY_NUMBER]):
        recipients = [num.strip() for num in MY_NUMBER.split(',') if num.strip()]
        print(f"📩 WhatsApp mesajı hazırlanıyor... ({len(recipients)} kişi)")
        try:
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            for number in recipients:
                try:
                    client.messages.create(from_=TWILIO_FROM, body=menu, to=number)
                    print(f"✅ WhatsApp: {number}")
                except Exception as e:
                    print(f"❌ WhatsApp Hata ({number}): {e}")
        except Exception as e:
             print(f"❌ Twilio Hatası: {e}")

    # 4. Send to Telegram (All)
    if TELEGRAM_TOKEN and all_telegram_recipients:
        # Join IDs into comma string for our helper function, or just loop here
        # Our helper expects string, let's just loop locally
        print(f"✈️ Telegram mesajı hazırlanıyor... ({len(all_telegram_recipients)} kişi)")
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        for chat_id in all_telegram_recipients:
            try:
                payload = {"chat_id": chat_id, "text": menu, "parse_mode": "Markdown"}
                requests.post(url, json=payload)
                print(f"✅ Telegram: {chat_id}")
            except Exception as e:
                print(f"❌ Telegram Hata: {e}")


if __name__ == "__main__":
    main()
