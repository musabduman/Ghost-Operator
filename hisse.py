# Dosya Adı: hisse.py
import yfinance as yf
import pandas as pd
from google import genai
import warnings
from ddgs import DDGS
import numpy as np
import ollama
import sys
import io
from ilk_zeka import borsa_muhasebe  # BU DOSYA AYNI KLASÖRDE OLMALI!

# Encoding ayarı (Türkçe karakter sorunu olmasın diye)
sys.stdout.reconfigure(encoding='utf-8')
warnings.filterwarnings('ignore')

# API KEY (Senin koddan aldım)
GOOGLE_API_KEY = "AIzaSyDTdKjIRw59wrOYJjNY-wqUVyhyCyclnM8"
client = genai.Client(api_key=GOOGLE_API_KEY)

# --- YARDIMCI FONKSİYONLAR (Senin yazdıkların, aynen korudum) ---

def sembol_temizle(metin):
    tr_map = str.maketrans("ığüşöçİĞÜŞÖÇ", "igusocIGUSOC")
    temiz_metin = metin.translate(tr_map).upper().strip()
    if not temiz_metin.endswith(".IS"):
        temiz_metin += ".IS"
    return temiz_metin

def teknik_analiz(df):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0))
    lose = (-delta.where(delta < 0, 0))
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_lose = lose.ewm(com=13, adjust=False).mean()
    rs = avg_gain / avg_lose

    df['RSI'] = 100 - (100 / (1 + rs))
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['Volume_signal'] = volume_trend(df, window=60)
    df['Volatility'] = calcu_volatility(df, window=20)
    df = bollinger(df, window=20)
    df = calcu_macd(df)
    df = calcu_pivot(df)
    return df

def temel_veriler(hisse):
    info = hisse.info
    temel = {
        "FK Orani": info.get('trailingPE', 'Veri Yok'),
        "PD/DD": info.get('priceToBook', 'Veri Yok'),
        "Kar Marji": info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 'Veri Yok',
        "Brut Kar": info.get('grossProfits', 'Veri Yok'),
        "Sektor": info.get('sector', 'Bilinmiyor'),
        "Oneri": info.get('recommendationKey', 'Yok')
    }
    return temel

def haber_verileri(sembol):
    haberler_listesi = []
    try:
        with DDGS() as ddgs:
            query = f"{sembol} hisse haberleri"
            result = ddgs.news(keywords=query, region="tr-tr", safesearch="off", max_results=3)
            for r in result:
                baslik = r.get('title', '')
                haberler_listesi.append(f"- {baslik}")
    except:
        haberler_listesi.append("Haber çekilemedi.")
    return haberler_listesi

def bollinger(df, window):
    df['SMA'] = df['Close'].rolling(window=20).mean()
    std = df['Close'].rolling(window=window).std()
    df['Upper'] = df['SMA'] + 2 * std
    df['Lower'] = df['SMA'] - 2 * std
    df['Width'] = (df['Upper'] - df['Lower']) / df['SMA']
    df['Signal'] = np.select([df['Close'] > df['Upper'], df['Close'] < df['Lower']], [1, -1], default=0)
    return df

def volume_trend(df, window=10):
    df['volume_signal'] = np.where(df['Volume'] > df['Volume'].rolling(window=window).mean(), 1, 0)
    return df['volume_signal']

def calcu_volatility(df, window=20):
    df['Returns'] = df['Close'].pct_change()
    df['Volatility'] = df['Returns'].rolling(window=window).std()
    return df['Volatility']

def calcu_macd(df):
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_signal'] = np.where(df['MACD'] > df['Signal_line'], 1, -1)
    return df

def calcu_pivot(df):
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['R1'] = (2 * df['Pivot']) - df['Low']
    df['S1'] = (2 * df['Pivot']) - df['High']
    return df

def muhasebeci(df):
    try:
        bot = borsa_muhasebe()
        sonuc = bot.analiz_et(df)
        return f"AI Modeli: %{sonuc['güven']} ihtimalle {sonuc['yön']} bekliyor."
    except Exception as e:
        return "Muhasebe modülü hata verdi."

def gemini_yorumla(temel, sembol, df, haberler_listesi, ai_rapor):
    # Telegram için çıktıyı kısalttım, çok uzun olunca okunmuyor
    son_veriler = df.tail(10).to_string()
    temel_metin = str(temel)
    haberler_metni = "\n".join(haberler_listesi)
    
    prompt = f"""
    Sen dünyanın en iyi hedge fonlarında çalışan bir borsa uzmanısın. 
    Sen karşındaki kişinin yatırım asistanısın; samimi, abartısız ve net bir dil kullanabilirsin (arkadaşça ama profesyonel). Sakın yatırım tavsiyesi verme sadece elindeki bilgileri yorumla !

    ÖNEMLİ: Yaptıgın son yorumda "Neden?" sorusuna cevap ver. Terimlere bogmadan, çokta uzatmadan, sonucun hangi veriden kaynaklandıgını açıkla. (Örn: "RSI 30'un altında oldugu için ucuz dedim" gibi).

    ELİNDEKİ VERİLER {sembol} İÇİN:

    1. TEMEL ANALİZ:
    {temel_metin}

    2. HABER AKIŞI (Son 1 Ay):
    {haberler_metni}
    (Haberlerin fiyat üzerindeki duygu durumunu -Sentiment- analiz et.)

    3. TEKNİK VERİLER (Son 20 Gün):
    {son_veriler}

    4. Aİ BOTU YARDIMI:
    {ai_rapor}
    (bu rapor tamamen sayısal verilerle hesaplanmıştır bunU AYNEN YAZDIR ve yorumunda kullan!)

    KARAR MEKANİZMAN (Bu kurallara sadık kal):
    • RSI: <30 (Aşırı Ucuz/Al Fırsatı), >70 (Aşırı Pahalı/Sat Fırsatı), 30-70 (Nötr/Trendi Takip Et).
    • MACD: 1 (Al/Yükseliş), -1 (Sat/Düşüş).
    • SMA 50/200: Fiyat ortalamanın üzerindeyse POZİTİF, altındaysa NEGATİF.
    • VOLUME_SIGNAL: 1 ise Yükseliş gerçek (Güven artır), 0 ise Yükseliş zayıf (Tuzak olabilir).
    • BOLLINGER: Width (Bant Genişligi) düşüyorsa "SIKIŞMA" var (Patlama Yakın). Signal 1 ise yukarı, 0 ise yatay.
    • PIVOT: Fiyat > Pivot ise Hedef R1. Fiyat < Pivot ise Destek S1.
    • VOLATİLİTE: Yüksekse stop seviyesini biraz daha geniş tut, düşükse dar tut.

    GÖREVİN:
    Tüm verileri (Temel + Teknik + Haber) birleştir. Teknik veriler "AL" derken Haberler "KÖTÜ" ise güven skorunu düşür. Çelişkileri belirt.

    ÇIKTI FORMATIN (Tam olarak bu başlıkları kullan):

    📊 GELECEK SENARYOSU:
    (İki üç cümle ile ne bekliyorsun? Yükseliş/Düşüş/Yatay)
    Karar mekanizmanda kullandıgın(MACD,SMA50,SMA200,VOLUME_SİGNAL,BOLLINGER,PİVOT,VOLATİLİTE,WİDTH) degerlerini burda satır satır göster ve yorumla !

    🎯 HEDEF FİYAT:
    (R1 veya teknik analize göre net bir rakam ver)

    🛑 STOP SEVİYESİ:
    (S1 veya risk yönetimine göre net bir rakam ver)

    🔥 GÜVEN SKORU:
    (0-100 arası. Neden bu puanı verdigini parantez içinde tek cümleyle açıkla.)

    📰 HABER VE TEMEL ETKİ:
    (Haberler teknigi destekliyor mu? Şirket temel olarak saglam mı?(kar marjını burda kullan) - En fazla 3 cümle)

    📈 TEKNİK ÖZET:
    (Göstergeler uyumlu mu? Hangi indikatör en baskın sinyali veriyor?)

    📌 SON KARAR:
    (GÜÇLÜ AL / AL / TUT / SAT / GÜÇLÜ SAT)
    VERILER:
    {son_veriler}

    AI RAPOR:
    {ai_rapor}
    """
    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini Hatası: {e}"

# --- İŞTE DEĞİŞEN KISIM (MAIN YOK, ARTIK OTOMATİK) ---

if __name__ == "__main__":
    # 1. Argüman Kontrolü (Bot buraya veri gönderecek)
    if len(sys.argv) < 2:
        print("HATA: Hisse kodu gönderilmedi.")
        sys.exit()
    
    try:
        ham_girdi = sys.argv[1] # Botun gönderdiği THYAO buraya gelir
        sembol = sembol_temizle(ham_girdi)
        
        print(f"🔍 {sembol} analiz ediliyor, lütfen bekleyin...")
        
        # 2. Verileri Çek
        hisse = yf.Ticker(sembol)
        df = hisse.history(period="1y")
        
        if df.empty:
            print("❌ Veri bulunamadı. Hisse kodunu kontrol edin.")
            sys.exit()
            
        # 3. Hesaplamaları Yap
        df = teknik_analiz(df)
        temel = temel_veriler(hisse)
        ai_rapor = muhasebeci(df)
        haberler_listesi = haber_verileri(sembol)
        
        # 4. Yorumu Al (Gemini)
        analiz_sonucu = gemini_yorumla(temel, sembol, df, haberler_listesi, ai_rapor)
        
        # 5. Sonucu Yazdır (Bot bunu okuyup sana atacak)
        print("\n" + analiz_sonucu)
        
        # Ollama denetçisini de istersen buraya print olarak ekleyebilirsin
        # Ama Telegram mesajı çok uzarsa bölünür, şimdilik Gemini yeterli.
        
    except Exception as e:
        print(f"💥 Kritik Hata: {e}")