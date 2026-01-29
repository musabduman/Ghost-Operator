from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

class borsa_muhasebe:
    def __init__(self):
        self.model=RandomForestClassifier(n_estimators=200, min_samples_split=10,random_state=42)
    
    def analiz_et(self,df):
        if df is None or df.empty:
            return {"yön":"VERİ YOK","güven":"0"}
        
        df['Getiri']=df['Close'].pct_change()
        df['Hacim_degisimi']=df['Volume'].pct_change()
        df['Oynaklık']=(df['High']-df['Low'])/df['Close']
        
        
        delta=df['Close'].diff()
        gain=(delta.where(delta>0,0))
        lose=(-delta.where(delta<0,0))
        avg_gain=gain.ewm(com=13, adjust=False).mean()
        avg_lose=lose.ewm(com=13, adjust=False).mean()
        
        rs=avg_gain/avg_lose
        
        df['RSI']=100-(100/(1+rs))
        df['SMA_50']=df['Close']/df['Close'].rolling(window=50).mean()
        
        df['Momentum']=df['Close']/df['Close'].shift(10)
        
        df.replace([np.inf,-np.inf], np.nan, inplace=True)
        
        self.ozellikler=['Getiri','Hacim_degisimi','Oynaklık','RSI','SMA_50','Momentum']
        
        df['Target']=(df['Close'].shift(-1)>df['Close']).astype(int)
        
        bugun=df.iloc[[-1]][self.ozellikler]
        gecmis=df.dropna()
        
        X=gecmis[self.ozellikler]
        Y=gecmis['Target']

        spilt=int(len(X)*0.8)
        X_train,X_test=X.iloc[:spilt],X.iloc[spilt:]
        Y_train,Y_test=Y.iloc[:spilt],Y.iloc[spilt:]

        self.model.fit(X,Y)
        if bugun.isnull().values.any():
            return {"yön": "HESAPLANAMADI (Eksik Veri)", "güven": 0}

        tahmin=self.model.predict(bugun)[0]
        olasılık=self.model.predict_proba(bugun)[0]

        if tahmin==1:
            return{"yön":"yükselis","güven":round(olasılık[1]*100, 2)}
        else:
            return{"yön":"düsüs","güven":round(olasılık[0]*100, 2)}
        
