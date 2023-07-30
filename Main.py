from Database import DbManager
from Opportunities import Ath, create_opportunity
from Contractor import req_ids

import time

DB_NAME = "watchlist.db"
# Function to specify type (G, D)


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
            create_opportunity(db)


if __name__ == "__main__":
    main()
