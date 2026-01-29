# 👻 Ghost Operator

> **"Görünmez ol. Her şeyi kontrol et. TEK SINIR HAYAL GÜCÜN."**

Ghost Operator, bilgisayarınızı Telegram üzerinden tamamen uzaktan yönetmenizi sağlayan, **Ollama (Yerel LLM)** destekli, yeni nesil bir komut merkezidir.

Siz dışarıdayken bilgisayarınız evde "hayalet" modunda çalışır. Telegram'dan tek bir mesaj atarak scriptleri çalıştırabilir, sistem durumunu sorgulayabilir veya yapay zeka ile sohbet edebilirsiniz.

## 💀 Yetenekler

* **⚡ Uzaktan İnfaz (Remote Execution):** Python scriptlerini veya sistem komutlarını uzaktan tetikleyin.
* **🧠 Hayalet Zeka:** Ollama entegrasyonu sayesinde, komutları doğal dil ile ("Bilgisayarı kapat", "Analiz yap") verebilirsiniz.
* **🔒 Güvenli Protokol:** Sadece yetkili `User ID` (Siz) komut gönderebilir. Yabancıları "Yassah Hemşerim" diyerek engeller.
* **📂 Modüler Yapı:** Yeni bir özellik mi lazım? Scripti klasöre atın, Ghost Operator onu anında tanır.

## 🛠️ Kurulum Protokolü

1.  **Depoyu Klonla:**
    ```bash
    git clone [https://github.com/musabduman/Ghost-Operator.git](https://github.com/musabduman/Ghost-Operator.git)
    ```

2.  **Gereksinimleri Yükle:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Kimlik Doğrulama:**
    `config_ornek.py` dosyasının adını `config.py` yapın ve bilgilerinizi girin:
    * `TOKEN`: BotFather'dan alınan gizli anahtar.
    * `MY_ID`: Telegram ID numaranız.
    * `MODEL`: Kullanılacak LLM (Örn: `llama3`).

4.  **Operasyonu Başlat:**
    ```bash
    python ghost_operator.py
    ```

## ⚠️ Yasal Uyarı
Bu araç, geliştiricinin kendi cihazlarını yönetmesi için tasarlanmıştır. **Token bilgilerinizi asla paylaşmayın.** Oluşabilecek güvenlik açıklarından kullanıcı sorumludur.

---
*Developed by [Musab Duman](https://github.com/musabduman)*