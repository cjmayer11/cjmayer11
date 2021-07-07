from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer
from datetime import datetime

class TestApp (EWrapper,EClient):
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


def start(self):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"

        order = Order()
        order.action = "BUY"
        order.totalQuantity = 1
        order.orderType = "LMT"
        order.lmtPrice = "1"

        self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
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