from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
         EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ", reqId, "Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low: ", bar.low, "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount)

app = IBapi()
app.connect('127.0.0.1', 7496, 122)
time.sleep(5)

contract = Contract()
contract.secType = "STK"
contract.symbol = "NIO"
contract.currency = "USD"
contract.exchange = "SMART"

app.reqHistoricalData(1, contract, "", "1 D", "1 min", "TRADES", 1, 1, False, [])
app.run()
time.sleep(10) #Sleep interval to allow time for incoming price data
app.disconnect()
