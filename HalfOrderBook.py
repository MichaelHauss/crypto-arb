from sortedcontainers import SortedDict

class HalfOrderBook(object):
	def __init__ (self, asc=True, orders=[]):
		self.ids    = {}
		self.orders = SortedDict()
		self.asc    = asc

		self.updateMany (orders)

	def update (self, order):
		assert "id" in order and "price" in order and "size" in order
		newId = order["id"]
		price = order["price"]

		# here, we are assuming that changing the size of an order
		# does not change its id but changing the price would (i.e. 
		# price of a specific order id doesn't change)
		assert newId not in self.ids \
			or self.ids[newId]["price"] == order["price"]

		# look up old order to calculate delta
		oldSize = self.ids[newId]["size"] if newId in self.ids else 0
		self.ids[newId] = order
		
		# update order book
		sizeDelta = order["size"] - oldSize
		if price not in self.orders:
			self.orders[price]  = sizeDelta
		else:
			self.orders[price] += sizeDelta

	def updateMany (self, orders):
		for order in orders:
			self.update (order)

	def best (self):
		return self.orders.peekitem (index=0 if self.asc else -1)

	def priceFor (self, size):
		assert size > 0
		found = 0
		cost  = 0
		for p in self.orderIter():
			newfind  = min (self.orders[p], size-found)
			cost    += newfind * p
			found   += newfind

			# min statement should ensure founnd never breaches size
			assert found <= size
			if found == size:
				return cost/found

		# order can't be filled on current book
		return None

	# returns size for price *or better*
	# for size at price only, use orders[price]
	def sizeFor (self, price):
		assert price >= 0
		found = 0
		for p in self.orderIter():
			if (p > price and self.asc) \
				or (p < price and not self.asc):
				return found
			found += self.orders[p]
		return found

	def orderIter(self):
		return self.orders if self.asc else reversed (self.orders)

	def __str__(self):
		return "\n".join ([
			str (self.orders[p]) + " @ " + str (p) for
			p in reversed(self.orders)
		])

def test():
	Asks = HalfOrderBook (asc=True, orders=[ 
		dict(id=1, price=100, size=6, meta="this"    ),
		dict(id=2, price=99,  size=3, meta="is"      ),
		dict(id=3, price=98,  size=2, meta="gdax"    ),
		dict(id=4, price=97,  size=7, neta="garbage" ),
	])

	Bids = HalfOrderBook (asc=False, orders=[ 
		dict(id=5, price=95,  size=1, meta="this"    ),
		dict(id=6, price=94,  size=5, meta="is"      ),
		dict(id=7, price=93,  size=5, meta="gdax"    ),
		dict(id=8, price=92,  size=4, neta="garbage" ),
	])

	print (
		"Inner sprd: " + str (Bids.best()[0]) + "-" 
		+ str (Asks.best()[0])
	)

	print ("Book:")
	print (Asks)
	print ("-------")
	print (Bids)

	print ("Ask for 10 coins --> "       + str (Asks.priceFor (10)))
	print ("Spend $99/coin gets me --> " + str (Asks.sizeFor  (99)))
	print ("Bid for 30 coins --> "       + str (Bids.priceFor (30)))
	print ("At $94/coin, can sell --> "  + str (Bids.sizeFor  (94)))

	print ("All clear!")

#test()