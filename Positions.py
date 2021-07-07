from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer

class TestApp (EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        self.start()

    def updatePortfolio(self, contract:Contract, position:float,
                        marketPrice:float, marketValue:float,
                        averageCost:float, unrealizedPNL:float,
                        realizedPNL:float, accountName:str):
        print("portfolioUpdate--", " Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
              contract.exchange, "Position:", "MarketPrice:", marketPrice, "MarketValue", marketValue, "AverageCost:",
              averageCost, "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

    def updateAccountValue(self, key:str, val:str, currency:str, accountName:str):
        print("accountValueUpdate--", "Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    def updateAccountTime(self, timeStamp:str):
        print("updateTime--", "Time:", timeStamp)

    def accountDownloadEnd(self, accountName:str):
        print("accountDownloadEnd--", "Account:", accountName)

    def start(self):
        self.reqAccountUpdates(True, "")


    def stop(self):
        self.reqAccountUpdates(False, "")
        self.done = True
        self.disconnect()

def main():
    app = TestApp()
    app.nextOrderId = 0
    app.connect('127.0.0.1', 7496, 0)

    Timer(5, app.stop).start()
    app.run()

if __name__=="__main__":
    main()