import subprocess
import json
import ollama
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import sys
from telegram.constants import ChatAction
import asyncio
try:
    import config
except ImportError:
    print("HATA: config.py dosyası bulunamadı! Lütfen config_ornek.py dosyasını düzenleyin.")
    sys.exit(1)

sys.stdout.reconfigure(encoding='utf-8')    

model=config.MODEL #buraya kendi yüklü modeliniz gelecek
token=config.TOKEN #buraya telegramdan alıcağınız token gelecek
my_id=config.MY_ID #buraya ise id numaranız gelecek

system_prompt="""Sen yardımsever ve zeki bir borsa asistanı ve kişisel asistansın. Uzaktan bilgisayarı kontrol etmek senin amacın ve bu amaç doğrultusunda eğer sana bir .py dosyası çalıştır derlerse onnu çalıştır
 ve outputu değiştirmeden yazdır ama eğer sohbet ederlerse sohbet havasında cevaplar ver.
SENİN İSMİN NEXUS.
Kullanıcı seninle sohbet ederse samimi cevaplar ver.

ANCAK, eğer kullanıcı senden bir hisse analizi veya başka bir hazır kodu çalıştırmanı, veri getirme veya işlem yapmanı isterse:
Cevabının en sonuna şu formatta bir etiket ekle:
###KOMUT: dosya_adı.py ARGUMAN###
Elindeki outputu da cevap olarak yaz json olarak çalış bir kod çalıştırmanı isterlerse.

ÖRNEKLER:
Kullanıcı: "Merhaba"
Sen: "Selam! Nasılsın?"

Kullanıcı: "THYAO hissesine bak"
Sen: "Hemen THYAO verilerini getiriyorum... ###KOMUT: hisse.py THYAO###"

Kullanıcı: "GARAN analizi yap"
Sen: "Garanti Bankası verilerine bakıyorum. ###KOMUT: hisse.py GARAN###"

ÖNEMLİ: Sadece kod çalıştırman gerektiğinde ###KOMUT: ...### ekle. Normal sohbette ekleme.
"""

async def mesaj_gelince(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    mesaj=update.message.text
    
    if user_id!=my_id:
        await update.message.reply_text("Yassah Hemşerim sizlik deil.")
        return
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        loop=asyncio.get_running_loop()
        cevap=await loop.run_in_executor(
            None,
            lambda:ollama.chat(
                model=model,
                messages=[
                    {'role':'system','content':system_prompt},
                    {'role':'user','content':mesaj}  
                ],      
            )
        )
        
        gelen_veri=cevap['message']['content']
        
        if "###KOMUT:" in gelen_veri:
            parcalar=gelen_veri.split("###KOMUT:")
            sohbet_kisimi=parcalar[0]
            komut_kisimi=parcalar[1].replace("###","").strip()
            if sohbet_kisimi:
                await update.message.reply_text(sohbet_kisimi)

            komut_detay=komut_kisimi.split()
            dosya_adi=komut_detay[0]
            argumanlar=komut_detay[1:]
            await update.message.reply_text(f"{dosya_adi} ile {argumanlar} çalıştırılıyor")
            tam_komut=["python",dosya_adi]+ argumanlar
            
            sonuc= subprocess.run(
                tam_komut,
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
        else:
            await update.message.reply_text(gelen_veri)
    except Exception as e:
        await update.message.reply_text(f"Bir hata oldu {e}")
            
if __name__ == '__main__':
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, mesaj_gelince))
    print("Bot Aktif! Telegramdan yazabilirsin.")
    app.run_polling()