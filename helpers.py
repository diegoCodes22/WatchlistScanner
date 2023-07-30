import datetime


def one_year_ago() -> datetime:
    return datetime.datetime.now() - datetime.timedelta(days=360)


def formatted_date(date: datetime):
    return date.strftime("%Y%m%d-%H:%M:%S")


def percentage_calculator(ath: float, cur: float) -> float:
    return round(((cur - ath) / ath) * 100, 2)


def calculate_op_priority(op: float) -> int:
    i = 1
    if op < 5:
        return 0
    else:
        for x in range(2, 10):
            if op > (5 * x) - 1 <= 40:
                i += 1
    return i
