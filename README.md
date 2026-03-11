# In-Memory Limit Order Book Engine

## Overview

This project implements an **in-memory limit order book engine** for a single instrument using Python.

The engine processes buy and sell orders sequentially, matches them using **price-time priority**, and prints trade executions as they occur.

Incoming orders interact with the existing order book. If a match is possible, a trade is executed. If not, the remaining quantity is stored in the order book as a resting order.

At the end of processing all input orders, the engine prints the **final state of the order book**.

---

## Features Implemented

The engine supports the following functionality:

* Limit orders
* Market orders (price = 0)
* Order matching using price-time priority
* Partial order fills
* Order cancellation
* Aggregated order book display (top price levels)

---

## Order Input Format

Orders are provided in the following format:

```
ORDER_ID SIDE PRICE QUANTITY
```

Example:

```
O1 BUY 100.50 10
O2 SELL 101.00 5
```

### Field Description

| Field    | Description                     |
| -------- | ------------------------------- |
| ORDER_ID | Unique identifier for the order |
| SIDE     | BUY or SELL                     |
| PRICE    | Order price                     |
| QUANTITY | Order size                      |

---

## Market Orders

Market orders are represented using:

```
PRICE = 0
```

These orders execute immediately against the **best available price** on the opposite side of the book.

Example:

```
O5 BUY 0 10
```

This will match against the lowest available sell price.

---

## Cancel Orders

Orders can be cancelled using:

```
CANCEL ORDER_ID
```

Example:

```
CANCEL O2
```

If the order exists in the order book, it is removed.

---

## Trade Output Format

When a trade occurs, the engine prints:

```
TRADE BUY_ORDER SELL_ORDER PRICE QUANTITY
```

Example:

```
TRADE O1 O3 100.50 8
```

---

## Final Order Book Output

After all orders are processed, the engine prints the remaining order book.

Example:

```
--- Book ---
ASK: 99.00 x 18
```

Quantities are **aggregated per price level**.

---

## Matching Logic

The engine follows **price-time priority**.

### Buy Order Matching

A buy order matches with the **lowest sell price** when:

```
BUY price >= SELL price
```

### Sell Order Matching

A sell order matches with the **highest buy price** when:

```
SELL price <= BUY price
```

Within the same price level, orders are matched **in the order they arrived (FIFO)**.

---

## Partial Fills

If the incoming order quantity is larger than the available quantity at the best price level:

* A trade is executed for the available quantity
* The remaining quantity continues matching or rests in the book

---

## Data Structures Used

The order book maintains two sides:

### Bid Side (BUY orders)

* Stored by price
* Highest price matched first

### Ask Side (SELL orders)

* Stored by price
* Lowest price matched first

Internally the implementation uses:

```
dictionary: price → deque(orders)
```

This allows:

* FIFO order execution at each price level
* efficient insertion and removal of orders

---

## Project Structure

```
In-Memory-Order-Book-Engine/

main.py
engine.py
order_book.py
order.py
input.txt
README.md
```

### main.py

Entry point of the program.
Reads orders from `input.txt`, parses them, and sends them to the matching engine.

### engine.py

Contains the **matching engine logic** responsible for processing orders and executing trades.

### order_book.py

Maintains the **bid and ask order books** and handles order insertion and cancellation.

### order.py

Defines the **Order class** used to represent individual orders.

---

## How to Run

Run the program using:

```
python main.py
```

The engine reads orders from:

```
input.txt
```

---

## Example Input

```
O1 BUY 100.50 10
O2 BUY 100.50 5
O3 SELL 100.50 8
O4 SELL 99.00 20
CANCEL O2
```

---

## Example Output

```
TRADE O1 O3 100.50 8
TRADE O1 O4 99.00 2
--- Book ---
ASK: 99.00 x 18
```

---

## Summary

This project demonstrates the core mechanics of an electronic trading order book, including:

* price-time priority matching
* order execution
* partial fills
* order cancellation
* maintaining an in-memory order book

The implementation focuses on **correct order matching and clear modular design**.
