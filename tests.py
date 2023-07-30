def calculate_op_priority(op: float) -> int:
    i = 1
    if op < 5:
        return 0
    else:
        for x in range(2, 9):
            if op > (5 * x) - 1 <= 40:
                i += 1
    return i

print(calculate_op_priority())