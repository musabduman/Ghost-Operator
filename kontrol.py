import config
import telebot
import os
import time
import pyautogui
import sys

TOKEN=config.TOKEN
my_id=config.MY_ID
bot=telebot.TeleBot(TOKEN)

def guvenlik(message=None):
    if message is None:
        return True
    if message.from_user.id==my_id:
        return True
    else:
        bot.reply_to(message,"Yassahh hemşerim")
        return False

def send_screenshot(message=None):
    if guvenlik(message):
        chat_id=message.chat.id if message else my_id
        bot.send_message(chat_id,"Ekran görüntüsü alınıyor..")
        screenshot_name="screenshot.png"
        pyautogui.screenshot(screenshot_name)

        with open(screenshot_name,'rb') as photo:
            bot.send_photo(chat_id,photo,caption="Anlık bilgisayarınızın durumu")
    os.remove(screenshot_name)

def close_to_computer(message=None):
    if guvenlik(message):
        chat_id=message.chat.id if message else my_id
        bot.send_message(chat_id,"Bilgisayar Kapatılıyor...")
        time.sleep(2)

        os.system("shutdown /s /t 1")
def lock_pc(message=None):
    if guvenlik(message):
        chat_id=message.chat.id if message else my_id
        bot.send_message(chat_id,"Bilgisayar kitleniyor..")
        time.sleep(2)

        os.system("rundll32.exe user32.dll,LockWorkStation")

if __name__=="__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("HATA: Hisse kodu gönderilmedi.")
        sys.exit()
    
    try:
        raw_input= sys.argv[1]
        ham_girdi = raw_input.replace("['","").replace("']","").replace("'","").strip().lower()
        
        if ham_girdi=="kapat":
            close_to_computer()
        elif ham_girdi=="kilitle":
            lock_pc()
        elif ham_girdi=="ss":
            send_screenshot()
    except:
        print(f"Bu komutlara uygun islem bulunamadi {ham_girdi}")


