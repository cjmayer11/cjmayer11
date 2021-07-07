from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
from threading import Timer
from ibapi.ticktype import *

import collections
import pandas as pd

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.data=collections.defaultdict(list)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.nextOrderId=orderId
        self.start()

    def contractDetails(self, reqId, contractDetails):
        self.data["conid"].append(contractDetails.contract.conId)
        self.data["symbol"].append(contractDetails.contract.localSymbol)

    def contractDetailsEnd(self, reqId):
        print("\ncontractDetails End\n")
        self.df=pd.DataFrame.from_dict(app.data)
        self.stop()

    def start(self):
        #self.reqSecDefOptParams(1, "AAPL", "", "STK", 265598)
        contract = Contract()
        contract.symbol = "ES"
        contract.secType = "CONTFUT"
        contract.exchange = "GLOBEX"
        self.reqContractDetails(1, contract)

    def stop(self):
        self.disconnect()
        print(self.df)
        #self.df.to_csv('options_test.csv')

def main():
    app = TestApp()
    app.connect('127.0.0.1', 7496, 126)
    app.run()