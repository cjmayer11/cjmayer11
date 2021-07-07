from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
from threading import Timer
from ibapi.ticktype import *
import time
from datetime import datetime
import pandas as pd

class FuturesMD(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.mdprice = {}
        self.mdsize = {}

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        print(datetime.now(), "priceUpdate", "Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price,
              end=' ')

    def tickSize(self, reqId, tickType, size):
        print(datetime.now(), "sizeUpdate", "Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)



class FuturesContract(Contract):
        def __init__(self, symbol, lastTrade, exch, tclass):
            Contract.__init__(self)
            self.symbol = symbol
            self.lastTradeDateOrContractMonth = lastTrade
            self.secType = "FUT"
            self.exchange = exch
            self.currency = "USD"
            self.tradingClass = tclass

app = FuturesMD()
app.connect('127.0.0.1', 7496, 101)

time.sleep(5)

#contract = FuturesContract("ES", "20210319", "GLOBEX", "ES")
#contract = FuturesContract("SI", "20210526", "NYMEX", "SIL")
contract = FuturesContract("SI", "20210526", "NYMEX", "SI")


app.reqMarketDataType(1)
app.reqMktData(1, contract, "", False, False, [])
app.run()

time.sleep(5)
app.disconnect()