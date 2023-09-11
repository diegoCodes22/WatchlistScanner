from ibapi.client import EClient, Contract
from ibapi.common import OrderId
from ibapi.contract import ContractDetails
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import EWrapper

from Database import DbManager


class PlaceOrder(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_id = 0
        self.multiplier = 0

    def nextValidId(self, orderId: int):
        new_contract = Contract()
        new_contract.conId = self.contract_id
        new_contract.exchange = "SMART"

        self.reqContractDetails(orderId, new_contract)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        order = Order()
        order.orderId = reqId
        order.action = "BUY"
        order.orderType = "MKT"
        order.totalQuantity = self.multiplier

        self.placeOrder(reqId, contractDetails.contract, order)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"OPEN ORDER: {contract.symbol} {order.action} {orderState.status} {orderState.commission}", end="\n\n")

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float,
                    permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"ORDER STATUS: Status: {status}\nFilled: {filled}\nFill price: {avgFillPrice}\n")
        if remaining == 0:
            self.disconnect()


    def place_order(self, contract_id: int, mult: int):
        self.contract_id = contract_id
        self.multiplier = mult


def executor(db: DbManager) -> None:
    order_app = PlaceOrder()
    for ops in db.get_opps():
        multiplier = ops["buy"] - ops["opportunities_taken"]
        if 0 < multiplier < 5:
            order_app.connect("127.0.0.1", 7497, 1002)
            order_app.place_order(ops["contract_id"], multiplier)
            order_app.run()
            db.update_opt(ops['contract_id'])
