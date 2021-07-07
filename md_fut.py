from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
from threading import Timer
from ibapi.ticktype import *
import time
from datetime import datetime

class IBapi(EWrapper, EClient):
    def __init__(self):
         EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId , tickType, price, attrib):
        print(datetime.now(), "priceUpdate","Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')

    def tickSize(self, reqId, tickType, size):
        print(datetime.now(), "sizeUpdate", "Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    

app = IBapi()
app.connect('127.0.0.1', 7496, 101)

time.sleep(5)

contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "GLOBEX"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "20210319"

app.reqMarketDataType(1)
app.reqMktData(1, contract, "", False, False, [])
app.run()

time.sleep(5)
app.disconnect()