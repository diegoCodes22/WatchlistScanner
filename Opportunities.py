from ibapi.client import EClient, Contract
from ibapi.ticktype import TickType
from ibapi.wrapper import EWrapper
from ibapi.common import BarData, TickerId, TickAttrib

from Database import DbManager

from helpers import *
import time


class Ath(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_id = 0
        self.ath = []

    def historicalData(self, reqId: int, bar: BarData) -> None:
        self.ath.append(bar.close)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.disconnect()

    def nextValidId(self, orderId: int) -> None:
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


class CurrentPrice(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_id = 0
        self.current_price = 0

    def nextValidId(self, orderId: int) -> None:
        new_contract = Contract()
        new_contract.conId = self.contract_id
        new_contract.exchange = "SMART"
        time.sleep(1)
        self.reqMarketDataType(2)
        self.reqMktData(orderId, new_contract, "", False, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        if tickType == 2:
            self.current_price = price

    def req_current(self, contract_id: int):
        self.contract_id = contract_id


def create_opportunity(db: DbManager):
    ath_app = Ath()
    cur_app = CurrentPrice()
    for c in db.select_contracts():
        ath_app.connect("127.0.0.1", 7497, 1000)
        if c["all_time_high"] == 0:
            ath_app.req_ath(c["contract_id"])
            ath_app.run()
            db.update_ath(max(ath_app.ath), c["contract_id"])
        else:
            cur_app.req_current(c["contract_id"])
            cur_app.run()
            op = percentage_calculator(max(ath_app.ath), cur_app.current_price)
            if op < 0:
                priority = calculate_op_priority(-op)
                if priority > 5:
                    print(f"SEVERE DROP IN {c['ticker']}. CHECK IMMEDIATELY!")
                    print(f"SEVERE DROP IN {c['ticker']}. CHECK IMMEDIATELY!")
                    print(f"SEVERE DROP IN {c['ticker']}. CHECK IMMEDIATELY!\nContinuing...")
                    time.sleep(3)

            else:
                # Update ath in db
                pass


