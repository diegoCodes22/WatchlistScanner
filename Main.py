from Database import DbManager
from Opportunities import scan_opportunities
from Contractor import req_ids

import time

DB_NAME = "watchlist.db"


def main():
    db = DbManager(DB_NAME)

    while True:
        time.sleep(1)
        i = int(input("Enter mode, or -1 for help: "))

        if i == -1:
            print('''Options are:\n\t0 Exit program\n\t1 Create contract ids\n\t2 Scan for opportunities
            \n\t3 Present watchlist\n\t4 Place orders''')
        elif i == 0:
            db.close_db()
            break
        elif i == 1:
            req_ids(db)
        elif i == 2:
            scan_opportunities(db)
        elif i == 3:
            db.present_watchlist()
        elif i == 4:
            print("W.I.P")
            # Print list of tickers with opportunities (not taken) and provide a space separated list of the stocks I
            # want to buy, the best would be to make it automatic, but for that I would need monthly cash flow


if __name__ == "__main__":
    main()
