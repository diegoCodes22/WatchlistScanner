from Database import DbManager
from Opportunities import scan_opportunities
from Contractor import req_ids
from Executor import executor

import time

DB_NAME = "watchlist.db"


# Fractional share are not yet supported by the API
# Add the case where I can't connect to TWS
# Save the console logs (for orders) in a CSV file

def main():
    db = DbManager(DB_NAME)

    while True:
        time.sleep(1)
        i = int(input('''\t0 Exit program\n\t1 Add to watchlist\n\t2 Scan watchlist\n\t3 Execute orders\n\t'''))

        if i == 0:
            db.close_db()
            break
        elif i == 1:
            req_ids(db)
        elif i == 2:
            scan_opportunities(db)
        elif i == 3:
            executor(db)


if __name__ == "__main__":
    main()
