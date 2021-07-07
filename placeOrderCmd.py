from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer
from datetime import datetime
from placeOrderAuto import *



app = IBapi()
app.nextOrderId = 0
app.connect('127.0.0.1', 7497, 0)
app.placeOrder(app.nextOrderId, app.placeOrderAuto.StockSym("IBM"), placeOrderAuto.stockOrd(app,"BUY", 1, "LMT", 1))
Timer(5, app.stop).start()
app.run()
