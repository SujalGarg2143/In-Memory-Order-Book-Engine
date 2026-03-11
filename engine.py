from order_book import OrderBook
from order import Order


class MatchingEngine:

    def __init__(self):
        self.book = OrderBook()
        self.time = 0

    def process_order(self, order_id, side, price, qty):

        self.time += 1
        order = Order(order_id, side, price, qty, self.time)

        if side == "BUY":
            self.match_buy(order)
        else:
            self.match_sell(order)

        if order.quantity > 0 and price != 0:
            self.book.add_order(order)

    def match_buy(self, order):

        asks = sorted(self.book.asks.keys())

        for price in asks:

            if order.price != 0 and price > order.price:
                break

            queue = self.book.asks[price]

            while queue and order.quantity > 0:

                sell_order = queue[0]

                trade_qty = min(order.quantity, sell_order.quantity)

                print(f"TRADE {order.id} {sell_order.id} {price} {trade_qty}")

                order.quantity -= trade_qty
                sell_order.quantity -= trade_qty

                if sell_order.quantity == 0:
                    queue.popleft()
                    del self.book.order_map[sell_order.id]

            if not queue:
                del self.book.asks[price]

            if order.quantity == 0:
                break

    def match_sell(self, order):

        bids = sorted(self.book.bids.keys(), reverse=True)

        for price in bids:

            if order.price != 0 and price < order.price:
                break

            queue = self.book.bids[price]

            while queue and order.quantity > 0:

                buy_order = queue[0]

                trade_qty = min(order.quantity, buy_order.quantity)

                print(f"TRADE {buy_order.id} {order.id} {price} {trade_qty}")

                order.quantity -= trade_qty
                buy_order.quantity -= trade_qty

                if buy_order.quantity == 0:
                    queue.popleft()
                    del self.book.order_map[buy_order.id]

            if not queue:
                del self.book.bids[price]

            if order.quantity == 0:
                break

    def cancel(self, order_id):
        self.book.remove_order(order_id)

    def print_book(self):

        print("--- Book ---")

        asks = sorted(self.book.asks.items())[:5]

        for price, orders in asks:
            qty = sum(o.quantity for o in orders)
            print(f"ASK: {price} x {qty}")

        bids = sorted(self.book.bids.items(), reverse=True)[:5]

        for price, orders in bids:
            qty = sum(o.quantity for o in orders)
            print(f"BID: {price} x {qty}")