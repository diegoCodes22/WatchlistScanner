from ibapi.client import EClient, Contract
from ibapi.contract import ContractDetails
from ibapi.wrapper import EWrapper
from ibapi.common import TickerId, BarData, HistogramData
from helpers import *
import time

DB_NAME = "watchlist.db"


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
            print(f"Unable to retrieve contract information for symbol {self.ticker}. Continuing...")
            self.disconnect()


class Opportunities(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_id = 0
        self.ath = []

    def historicalData(self, reqId: int, bar: BarData) -> None:
        self.ath.append(bar.close)

    def historicalDataEnd(self, reqId:int, start:str, end:str):
        self.disconnect()

    def nextValidId(self, orderId:int) -> None:
        new_contract = Contract()
        new_contract.conId = self.contract_id
        new_contract.exchange = "SMART"
        time.sleep(1)
        self.reqHistoricalData(orderId, new_contract, formatted_date(one_year_ago()), "1 Y", "1 day", "TRADES", 1, 1,
                               False, [])

    def req_ath(self, contract_id: int) -> None:
        self.contract_id = 0
        self.contract_id = contract_id
        self.ath = []


def req_ids(db: DbManager, app: Contractor) -> None:
    for c in db.select_no_contract_id():
        app.connect("127.0.0.1", 7497, 1000)
        app.create_id(c["ticker"])
        app.run()

    for new_id in app.ids:
        db.update_contract_id(new_id[0], new_id[1])


def create_opportunity(db: DbManager, app: Opportunities):
    for c in db.select_contracts():
        if c["all_time_high"] == 0:
            app.connect("127.0.0.1", 7497, 1000)
            app.req_ath(c["contract_id"])
            app.run()
            db.update_ath(max(app.ath), c["contract_id"])
        else:
            pass  # compare current price with ath


def main():
    db = DbManager(DB_NAME)

    while True:
        time.sleep(1)
        i = int(input("Enter mode, or -1 for help: "))

        if i == -1:
            print('''
    Options are:
        0 Exit program
        1 Create contract ids
        2 Scan for opportunities
                ''')
        elif i == 0:
            break
        elif i == 1:
            app = Contractor()
            req_ids(db, app)
        elif i == 2:
            app = Opportunities()
            create_opportunity(db, app)


if __name__ == "__main__":
    main()
