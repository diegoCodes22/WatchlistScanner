from Database import DbManager
from Opportunities import scan_opportunities
from Contractor import req_ids

import time

DB_NAME = "watchlist.db"
# Add the times bought for that stock


def main():
    db = DbManager(DB_NAME)

    while True:
        time.sleep(1)
        i = int(input("Enter mode, or -1 for help: "))

        if i == -1:
            print('''Options are:\n\t0 Exit program\n\t1 Create contract ids\n\t2 Scan for opportunities\n''')
        elif i == 0:
            db.close_db()
            break
        elif i == 1:
            req_ids(db)
        elif i == 2:
            scan_opportunities(db)  # I need to add a column for opportunities taken,
            # if not, even if I buy, it will still show an opportunity
        elif i == 3:
            db.present_watchlist()
        elif i == 4:
            pass
            # Create and place order for specified symbol (One at a time)


if __name__ == "__main__":
    main()
