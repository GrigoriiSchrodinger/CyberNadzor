from loader import db
from src.blockchain import BitcoinAPI


class RaceTrack(BitcoinAPI):
    async def track_crypto(self):
        # tickers = self.get(end_point="/tickers")
        # for ticker in tickers:
        #     print(ticker)
        date = db.fetchall("SELECT * FROM below_track")
        print(date)



