from ibapi.client import *
from ibapi.wrapper import *


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        print(f"contract details {contractDetails.contract.conId}")

    def contractDetailsEnd(self, reqId:int):
        print(f"End")
        self.disconnect()


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 1000)

    mycontract = Contract()
    mycontract.symbol = input("Enter stock ticker: ")
    mycontract.secType = "STK"
    mycontract.exchange = "SMART"
    mycontract.currency = "USD"
    mycontract.primaryExchange = "ISLAND"

    app.reqContractDetails(1, mycontract)

    app.run()


if __name__ == "__main__":
    main()

