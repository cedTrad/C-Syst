import joblib
import sqlalchemy
from .features import get_pipeline, compute_daily_volatility

class ML:
    
    def __init__(self, data):
        self.data = data.copy()
    
    def get_model(self):
        model = joblib.load('system/decision/strategies/model.pkl')
        return model
    
    def processing(self):
        self.data.columns = [str(col) if isinstance(col, sqlalchemy.sql.elements.quoted_name) else col for col in self.data.columns]
        self.data['volatility'] = compute_daily_volatility(self.data['close'])
        pipe = get_pipeline()
        pipe.fit_transform(self.data)
        
        
    def run(self, bar=-1):
        self.processing()
        model = self.get_model()
        x = self.data.iloc[bar].values.reshape([1, -1])
        side = model.predict(x)[0]
        proba = model.predict_proba(x)[:,1][0]
        return side, proba