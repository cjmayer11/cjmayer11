from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
         EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)

app = IBapi()
app.connect('127.0.0.1', 7496, 45)
time.sleep(5)

contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "NASDAQ"

app.reqContractDetails(1, contract)
app.run()

app.disconnect()