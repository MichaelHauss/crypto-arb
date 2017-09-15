import heapq
from sortedcontainers import SortedDict

class HalfOrderBook(object):
	def __init__ (self, asc=True):
		self.ids = {}
		self.sizes = SortedDict()
		self.asc = asc

	def update (self, order):
		assert "id" in order and "price" in order and "size" in order
		newId = order["id"]
		price = order["price"]

		# here, we are assuming that changing the size of an order
		# does not change its id but changing the price would (i.e. 
		# price of a specific order id doesn't change)
		assert newId not in self.ids \
			   or self.ids[newId]["price"] == order["price"]

		oldSize = self.ids[newId]["size"] if newId in self.ids else 0
		self.ids[newId] = order
		
		sizeDelta = order["size"] - oldSize
		if price not in self.sizes :
			self.sizes[price] = sizeDelta
		else :
			self.sizes[price] += sizeDelta

	def updateMany (self, orders):
		for order in orders:
			self.update (order)

	def best (self):
		return self.sizes.peekitem (index=0 if self.asc else -1)

	def priceFor (self, size):
		assert size > 0
		found = 0
		cost = 0
		for px in self.sizes if self.asc else reversed (self.sizes):
			newfind = min (self.sizes[px],size-found)
			cost += newfind * px
			found += newfind

			# min statement should ensure founnd never breaches size
			assert found <= size
			if found == size:
				return cost/found

		# order can't be filled on current book
		return None

	def sizeFor (self, price):
		assert price >= 0
		found = 0
		for px in self.sizes if self.asc else reversed (self.sizes):
			if (px > price and self.asc) \
				or (px < price and not self.asc):
				return found
			found += self.sizes[px]
		return found

	def __str__(self):
		# for the normal (small) size of order books, this should be 
		# faster than any StringBuilder type optimizations
		bookStr = ""
		newLine = ""
		for px in reversed(self.sizes):
			bookStr += newLine
			bookStr += str (self.sizes[px]) + " @ " + str (px)
			newLine = "\n"
		return bookStr

def test():
	Asks = HalfOrderBook (asc=True)
	Bids = HalfOrderBook (asc=False)
	Asks.updateMany ([ 
		dict(id=1, price=100, size=6, meta="this"    ),
		dict(id=2, price=99,  size=3, meta="is"      ),
		dict(id=3, price=98,  size=2, meta="gdax"    ),
		dict(id=4, price=97,  size=7, neta="garbage" ),
	])

	Bids.updateMany ([ 
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

	print ("Ask for 10 coins --> " +  str (Asks.priceFor(10)))
	print ("Spend $99/coin gets me --> " + str (Asks.sizeFor(99)))
	print ("Bid for 30 coins --> " +  str (Bids.priceFor(30)))
	print ("At $94/coin, can sell --> " + str (Asks.sizeFor(94)))
test()