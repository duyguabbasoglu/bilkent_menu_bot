import scraper
import pywhatkit
import os
import time

PHONE_FILE = "phone_number.txt"

def get_phone_number():
    if os.path.exists(PHONE_FILE):
        with open(PHONE_FILE, "r") as f:
            number = f.read().strip()
            if number:
                return number
    
    print("👋 Merhaba! İlk çalıştırma için telefon numarası gerekli.")
    print("Örnek: +905551234567 (Lütfen ülke kodu ile giriniz)")
    number = input("Telefon Numarası: ").strip()
    
    if number:
        with open(PHONE_FILE, "w") as f:
            f.write(number)
        print("✅ Numara kaydedildi.")
        return number
    else:
        print("❌ Geçersiz numara.")
        return None

def main():
    print("🍽️ Menü indiriliyor...")
    menu = scraper.get_menu()
    
    if not menu:
        print("❌ Menü alınamadı.")
        return

    print("📩 WhatsApp mesajı hazırlanıyor...")
    phone_number = get_phone_number()
    
    if not phone_number:
        return

    print(f"🚀 Gönderilecek numara: {phone_number}")
    print("⚠️ WhatsApp Web açılacak ve mesaj gönderilecek. Lütfen tarayıcıyı kapatmayın.")
    
    try:
        # wait_time: time to wait for loading WhatsApp, tab_close: close tab after sending
        pywhatkit.sendwhatmsg_instantly(phone_number, menu, wait_time=15, tab_close=True, close_time=5)
        print("✅ Mesaj gönderildi (veya gönderilmek üzere sıraya alındı).")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

if __name__ == "__main__":
    main()
