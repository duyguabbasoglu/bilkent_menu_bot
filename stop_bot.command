#!/bin/bash
# Remove the job
SCRIPT_PATH="/Users/dyliax/Desktop/yemekhane_bot/run_menu.command"
crontab -l | grep -v "$SCRIPT_PATH" | crontab -

echo "✅ Yemekhane Botu zamanlayıcısı iptal edildi."
echo "🛑 Artık otomatik mesaj gönderilmeyecek."
