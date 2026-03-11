from engine import MatchingEngine


engine = MatchingEngine()


def process_line(line):

    parts = line.strip().split()

    if parts[0] == "CANCEL":

        engine.cancel(parts[1])
        return

    order_id = parts[0]
    side = parts[1]
    price = float(parts[2])
    qty = int(parts[3])

    engine.process_order(order_id, side, price, qty)


def main():

    with open("input.txt") as f:
        for line in f:
            process_line(line)

    engine.print_book()


if __name__ == "__main__":
    main()