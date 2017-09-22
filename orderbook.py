import HalfOrderBook

class OrderBook(object):
	def __init__ (self, priceCcy="USD", sizeCcy="BTC", fee=0.0025):
		self.orders   = dict(
			bid=HalfOrderBook(asc=False),
			ask=HalfOrderBook(asc=True)
		)
		self.priceCcy = priceCcy
		self.sizeCcy  = sizeCcy
		self.fee	  = fee

	# order is a dictionary that contains: side ("bid"/"ask"), id,
	# price, size
	def update (self, order):
		assert "side" in order
		self.orders[order.side].update (order)

	def updateMany (self, orders):
		for order in orders:
			self.update (order)

def test():
	OB = OrderBook();

	OB.updateMany ([ 
		dict(side="ask", id=1, price=100, size=6, meta="this"    ),
		dict(side="ask", id=2, price=99,  size=3, meta="is"      ),
		dict(side="ask", id=3, price=98,  size=2, meta="gdax"    ),
		dict(side="ask", id=4, price=97,  size=7, neta="garbage" ),

		dict(side="bid", id=5, price=95,  size=1, meta="this"    ),
		dict(side="bid", id=6, price=94,  size=5, meta="is"      ),
		dict(side="bid", id=7, price=93,  size=5, meta="gdax"    ),
		dict(side="bid", id=8, price=92,  size=4, neta="garbage" ),
	])


test()