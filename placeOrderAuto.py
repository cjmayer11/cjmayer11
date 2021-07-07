from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer
from datetime import datetime

class IBapi (EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId , status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print(datetime.now(), "--orderStatus--", " ID:", orderId, "Status:", status, "Filled:", filled, "Remaining:", remaining, "LastFillPrice:", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print(datetime.now(), "--openOrder--", " ID:", orderId, contract.symbol, contract.secType, "@",contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print(datetime.now(), "--execDetails--", " ID:", reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def stockSym(self, sym):
        contract = Contract()
        contract.symbol = sym
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"
        return (contract)

    def stockOrd(self, side, qty, tif, px):
        order = Order()
        order.action = side
        order.totalQuantity = qty
        order.orderType = tif
        order.lmtPrice = px
        return(order)

    def start(self):
        self.placeOrder(self.nextOrderId, self.stockSym("AAPL"), self.stockOrd("BUY", 1, "LMT", 1))

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    app = IBapi()
    app.nextOrderId = 0
    app.connect('127.0.0.1', 7497, 0)



    Timer(5, app.stop).start()
    app.run()


if __name__=="__main__":
    main()