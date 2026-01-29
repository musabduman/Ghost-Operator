# 🧠 AI Command Center: Bilgisayarını Chat ile Yönet

> **"Tek sınır, hayal gücünüz."**

Bu proje, sıradan bir botu değildir. Bilgisayarınızda çalışan yerel bir LLM (Ollama) ile Telegram'ı birbirine bağlayan, doğal dilden anlayan bir **Otomasyon Merkezidir**.

Siz Telegram'dan **"Bana THYAO hissesini yorumla"** dersiniz, yapay zeka bunu anlar, ilgili Python scriptini (`hisse.py`) bulur, çalıştırır ve sonucu size geri döner.

## 🌟 Neler Yapabilir? (Şimdilik)
Sistemin yetenekleri, `scriptler` klasörüne atacağınız dosyalara bağlıdır. Şu an yüklü modüller:

* **📈 Borsa Analizi:** "Ereğli hissesi ne durumda?" dediğinizde teknik ve temel analiz yapar.
* **🐍 Python Testi:** "Ekrana Ahmet yazdır" dediğinizde basit test scriptlerini çalıştırır.
* **🚀 Gelecek Potansiyeli:** Bilgisayarı kapatma, mail atma, dosya yedekleme... Sadece yeni bir script ekleyin ve yapay zekaya ne yapması gerektiğini söyleyin.

## 🛠️ Kurulum

1.  **Projeyi İndir:**
    ```bash
    git clone [https://github.com/musabduman/Borsa-Yapay-Zeka-Asistani.git](https://github.com/musabduman/Borsa-Yapay-Zeka-Asistani.git)
    ```

2.  **Gereksinimleri Yükle:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ollama'yı Kur:**
    Bilgisayarınızda [Ollama](https://ollama.com/) kurulu olmalı ve bir model (örn: `llama3` veya `gemma`) indirilmiş olmalıdır.

4.  **Ayarları Yap:**
    `telegram_control.py` dosyasını açın ve şu alanları doldurun:
    * `model`: Kullandığınız Ollama modeli (örn: "llama3")
    * `token`: BotFather'dan alınan Telegram Tokenı
    * `my_id`: Sadece sizin kullanmanız için Telegram ID'niz

## ▶️ Çalıştırma
Sistemi başlatmak için:
```bash
python telegram_control.py