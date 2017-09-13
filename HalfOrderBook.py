import heapq

class HalfOrderBook(object):
	def __init__ (self,minHeap=True):
		self.ids = {}
		self.prices = []
		self.sizes = {}
		self.minHeap = 2*minHeap - 1 #store as +/-1

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
			heapq.heappush (self.prices,self.minHeap*price)
			self.sizes[price] = sizeDelta
		else :
			self.sizes[price] += sizeDelta

	def updateMany (self, orders):
		for order in orders:
			self.update (order)

	def best (self):
		price = self.minHeap * self.prices[0]
		size = self.sizes[price]
		return dict(price=price, size=size)

def test():
	Mins = HalfOrderBook ()
	Mins.updateMany ([ 
		dict(id=1, price=100, size=6, meta="this"    ),
		dict(id=2, price=99,  size=3, meta="is"      ),
		dict(id=3, price=100, size=2, meta="gdax"    ),
		dict(id=2, price=99,  size=7, neta="garbage" ),
	])

	print(Mins.ids)
	print(Mins.prices)
	print(Mins.sizes)
	print(Mins.best())
	
	Maxs = HalfOrderBook (minHeap=False)
	Maxs.updateMany ([ 
		dict(id=1, price=100, size=6, meta="this"    ),
		dict(id=2, price=99,  size=3, meta="is"      ),
		dict(id=3, price=100, size=2, meta="gdax"    ),
		dict(id=2, price=99,  size=7, neta="garbage" ),
	])

	print(Maxs.ids)
	print(Maxs.minHeap)
	print(Maxs.prices)
	print(Maxs.sizes)
	print(Maxs.best())

test()