from sortedcontainers import SortedDict
from constants import OrderType

class HalfOrderBook():
	def __init__ (self, asc=True, orders=[]):
		"""
		If this object represents bids, use <asc=false> to sort in descending order.
		If this object represents offers, use <asc=true> to sort in ascending order.
		Orders are represented as dictionaries containing:
		\"id\"
		\"price\"
		\"size\"
		"""
		self.ids    = {}
		self.orders = SortedDict()
		self.asc    = asc

		self.update_many(orders)

	def update (self, order):
		assert "id" in order and "price" in order and "size" in order
		newId = order["id"]
		price = order["price"]

		# We assume it is possible to maintain the same order ID
		# when changing size, but not when changing price.
		assert newId not in self.ids \
			or self.ids[newId]["price"] == order["price"]

		# Check if the order already existsand update order index (self.ids)
		oldSize = self.ids[newId]["size"] if newId in self.ids else 0
		self.ids[newId] = order
		
		# Update optimized order book data structure (self.orders)
		sizeDelta = order["size"] - oldSize
		if price not in self.orders:
			self.orders[price]  = sizeDelta
		else:
			self.orders[price] += sizeDelta

	def update_many (self, orders):
		for order in orders:
			self.update(order)

	def best (self):
		"""Returns the single best order"""
		return self.orders.peekitem (index=0 if self.asc else -1)

	def price_for (self, size):
		"""Returns the best average price per unit for an order of a given <size>"""
		assert size > 0
		found = 0
		cost  = 0
		for p in self.order_iter():
			newfind  = min (self.orders[p], size-found)
			cost    += newfind * p
			found   += newfind

			# Min statement ensures found never breaches size
			assert found <= size
			if found == size:
				return cost/found

		# Order can't be filled on current book
		return None

	def size_for (self, price):
		"""Returns the available size of open orders for <price> or better"""
		assert price >= 0
		found = 0
		for p in self.order_iter():
			if (p > price and self.asc) \
				or (p < price and not self.asc):
				return found
			found += self.orders[p]
		return found

	def order_iter(self):
		return self.orders if self.asc else reversed (self.orders)

	def __str__(self):
		return "\n".join ([
			str (self.orders[p]) + " @ " + str (p) for
			p in reversed(self.orders)
		])

def test():

	AskOrders = [dict(id=1, price=100, size=6, meta="this", side=OrderType.ASK   ),
				dict(id=2, price=99,  size=3, meta="is", side=OrderType.ASK      ),
				dict(id=3, price=98,  size=2, meta="gdax", side=OrderType.ASK    ),
				dict(id=4, price=96,  size=7, neta="garbage", side=OrderType.ASK ),
	]

	BidOrders = [dict(id=5, price=95,  size=1, meta="this", side=OrderType.BID   ),
				dict(id=6, price=94,  size=5, meta="is", side=OrderType.BID      ),
				dict(id=7, price=93,  size=5, meta="gdax", side=OrderType.BID    ),
				dict(id=8, price=92,  size=4, neta="garbage", side=OrderType.BID ),
	]

	Asks = HalfOrderBook (asc=True, orders=AskOrders)
	Bids = HalfOrderBook (asc=False, orders=BidOrders)

	print("Ask for 10 coins --> "       + str (Asks.price_for (10)))
	print("Spend $99/coin gets me --> " + str (Asks.size_for  (99)))
	print("Bid for 30 coins --> "       + str (Bids.price_for (30)))
	print("At $94/coin, can sell --> "  + str (Bids.size_for  (94)))

#test()