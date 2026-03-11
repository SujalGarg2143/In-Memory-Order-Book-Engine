from collections import defaultdict, deque
from order import Order


class OrderBook:

    def __init__(self):
        self.bids = defaultdict(deque)
        self.asks = defaultdict(deque)
        self.order_map = {}

    def add_order(self, order):

        if order.side == "BUY":
            self.bids[order.price].append(order)
        else:
            self.asks[order.price].append(order)

        self.order_map[order.id] = order

    def remove_order(self, order_id):

        if order_id not in self.order_map:
            return

        order = self.order_map[order_id]

        book = self.bids if order.side == "BUY" else self.asks
        queue = book[order.price]

        for o in queue:
            if o.id == order_id:
                queue.remove(o)
                break

        if not queue:
            del book[order.price]

        del self.order_map[order_id]