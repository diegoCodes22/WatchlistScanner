from ibapi.client import EClient, Contract
from ibapi.contract import ContractDetails
from ibapi.wrapper import EWrapper
from ibapi.common import TickerId

from Database import DbManager

import time


class Contractor(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.ticker = None
        self.ids = []

    def contractDetails(self, reqId: int, contractDetails: ContractDetails) -> None:
        self.ids.append([self.ticker, contractDetails.contract.conId])

    def contractDetailsEnd(self, reqId: int) -> None:
        self.disconnect()

    def create_id(self, ticker) -> None:
        self.ticker = None
        self.ticker = ticker

        new_contract = Contract()
        new_contract.symbol = self.ticker
        new_contract.secType = "STK"
        new_contract.exchange = "SMART"
        new_contract.currency = "USD"
        new_contract.primaryExchange = "ISLAND"
        time.sleep(1)

        self.reqContractDetails(1, new_contract)

    def error(self, reqId: TickerId, errorCode: int, errorString: str, advancedOrderRejectJson="") -> None:
        super().error(reqId, errorCode, errorString)
        if errorCode == 200:
            print(f"Unable to retrieve contract information for symbol {self.ticker}, you will have to add it manually."
                  f" Continuing...")
            self.disconnect()


def req_ids(db: DbManager) -> None:
    app = Contractor()
    while True:
        symbols = (input("Enter symbols or -1 for help: ")).upper()
        if symbols == "-1":
            print("Enter space separated tickers for the stocks you wish to add")
        else:
            symbols = list(symbols.split(" "))
            for symbol in symbols:
                app.connect("127.0.0.1", 7497, 1000)
                app.create_id(symbol)
                app.run()

            for new_id in app.ids:
                db.insert_ticker(new_id[0])
                db.update_contract_id(new_id[0], new_id[1])
            break
