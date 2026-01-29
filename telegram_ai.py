import subprocess
import json
import ollama
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import sys
try:
    import config
except ImportError:
    print("HATA: config.py dosyası bulunamadı! Lütfen config_ornek.py dosyasını düzenleyin.")
    sys.exit(1)

sys.stdout.reconfigure(encoding='utf-8')    

model=config.MODEL #buraya kendi yüklü modeliniz gelecek
token=config.TOKEN #buraya telegramdan alıcağınız token gelecek
my_id=config.MY_İD #buraya ise id numaranız gelecek

system_prompt="""Sen bir bilgisayar asistanısın. Gelen isteği analiz et.
SADECE JSON formatında cevap ver. Yorum yapma.

Mevcut Scriptler:
1. 'deneme.py' -> Parametreler: [isim, sayı]
2. 'hisse.py' -> Parametreler: [hisse_kodu]

Örnek Cevap Formatı:
{"dosya": "deneme.py", "args": ["Ahmet", "50"]}"""

async def mesaj_gelince(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    user_id=update.effective_user.id
    mesaj=update.message.text
    if user_id!=my_id:
        await update.message.reply_text("Yassah Hemşerim sizlik deil.")
        return
    else:
        await update.message.reply_text("Sistem baslatıldı...")
        try:
            cevap=ollama.chat(
                model=model,
                messages=[
                    {'role':'system','content':system_prompt},
                    {'role':'user','content':mesaj}  
                ],
                format='json'
            )
            veri=json.loads(cevap['message']['content'])
            dosya=veri.get("dosya")
            argumanlar=veri.get("args",[])

            if not dosya:
                await update.message.reply_text("Bunu yapıcak bir kod bulunamadı..🤔")
                return
            komut_listesi=["python",dosya]+ [str(arg) for arg in argumanlar]
            sonuc= subprocess.run(
                komut_listesi,
                capture_output=True,
                text=True,
                timeout=120,
                encoding='utf-8',
                errors='replace'
                )
            if sonuc.returncode==0:
                await update.message.reply_text(f"Sonuc {sonuc.stdout}")
                return
            else:
                await update.message.reply_text(f"HATA {sonuc.stderr}")
        except Exception as e:
            await update.message.reply_text(f"Bir hata oldu {e}")
            
if __name__ == '__main__':
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, mesaj_gelince))
    print("Bot Aktif! Telegramdan yazabilirsin.")
    app.run_polling()