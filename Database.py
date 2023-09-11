import sqlite3


class DbManager:
    def __init__(self, db_name):
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur

    def close_db(self) -> None:
        self.cur.close()

    def insert_ticker(self, ticker: str) -> None:
        self.cur.execute('INSERT INTO Watchlist(ticker) VALUES(?)', (ticker,))
        self.conn.commit()
        # maybe make it return primary key

    def update_contract_id(self, ticker: str, contract_id: int) -> None:
        self.cur.execute('UPDATE Watchlist SET contract_id = ? WHERE ticker = ?', (contract_id, ticker))
        self.conn.commit()

    def select_no_contract_id(self) -> list:
        self.cur.execute('SELECT * FROM Watchlist WHERE (contract_id = 0)')
        return self.cur.fetchall()

    def select_contracts(self) -> list:
        self.cur.execute('SELECT * FROM Watchlist WHERE (contract_id != 0)')
        return self.cur.fetchall()

    def update_ath(self, ath: float, contract_id: int) -> None:
        self.cur.execute('UPDATE Watchlist SET all_time_high = ? WHERE contract_id = ?', (ath, contract_id))
        self.conn.commit()

    def update_priority(self, priority: int, contract_id: int) -> None:
        self.cur.execute('UPDATE Watchlist SET buy = ? WHERE contract_id = ?', (priority, contract_id))
        self.conn.commit()

    def update_last(self, current: float, contract_id: int) -> None:
        self.cur.execute('UPDATE Watchlist SET last_price = ? WHERE contract_id = ?', (current, contract_id))
        self.conn.commit()

    def present_watchlist(self):
        self.cur.execute('SELECT ticker, buy, all_time_high, last_price, opportunities_taken FROM Watchlist')
        for i in self.cur.fetchall():
            print(f"{i['ticker']} [ {i['buy']} ]  ( {i['opportunities_taken']} ) "
                  f"-ath {i['all_time_high']} -last {i['last_price']}", end="\n\n")

    def get_opps(self):
        self.cur.execute('SELECT contract_id, buy, opportunities_taken FROM Watchlist')
        return self.cur.fetchall()

    def update_opt(self, contract_id: int):
        self.cur.execute('UPDATE Watchlist SET opportunities_taken = buy WHERE contract_id = ?', (contract_id, ))
        self.conn.commit()
