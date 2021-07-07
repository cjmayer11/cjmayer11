from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper
from ibapi.common import *
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
         EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ", reqId, "Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low: ", bar.low, "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount)
        self.df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])


app = IBapi()
app.connect('127.0.0.1', 7496, 124)
time.sleep(5)

contract = Contract()
contract.symbol = "ES"
contract.secType = "CONTFUT"
contract.exchange = "GLOBEX"

app.reqHistoricalData(4, contract, "", "1 D", "1 min", "TRADES", 1, 1, True, [])
app.run()
time.sleep(10) #Sleep interval to allow time for incoming price data
app.disconnect()
