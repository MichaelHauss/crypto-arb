from HalfOrderBook import HalfOrderBook
from constants import OrderType, Unit, Fees

class OrderBook():
	def __init__ (self, priceCcy=Unit.USD, sizeCcy=Unit.BTC, fee=Fees.GDAX, askOrders=[], bidOrders=[]):
		"""
		Default price is in USD and size in BTC. Default fee is 0.0025
		Orders are represented as dictionaries containing:
		\"id\"
		\"price\"
		\"size\"
		"""
		self.orders   = dict(
			bid=HalfOrderBook(asc=False),
			ask=HalfOrderBook(asc=True)
		)
		self.priceCcy = priceCcy
		self.sizeCcy  = sizeCcy
		self.fee	  = fee

		self.update_many(askOrders, OrderType.ASK)
		self.update_many(bidOrders, OrderType.BID)

	def update (self, order, orderType):
		self.orders[orderType.value].update(order)

	def update_many (self, orders, orderType):
		for order in orders:
			self.update (order, orderType)

	def __str__(self):
		return "Price Currency: " + self.priceCcy.value + "\nSize Currency: " + self.sizeCcy.value + \
				"\n\nInner spread: " + str(self.orders[OrderType.BID.value].best()[0]) + "-" + str (self.orders[OrderType.ASK.value].best()[0]) + \
				"\n\nBook:\n\n" + str(self.orders[OrderType.ASK.value]) + "\n--------\n" + str(self.orders[OrderType.BID.value])

def test():

	AskOrders = [dict(id=1, price=100, size=6, meta="this"   ),
				dict(id=2, price=99,  size=3, meta="is"      ),
				dict(id=3, price=98,  size=2, meta="gdax"    ),
				dict(id=4, price=96,  size=7, neta="garbage" ),
	]

	BidOrders = [dict(id=5, price=95,  size=1, meta="this"  ),
				dict(id=6, price=94,  size=5, meta="is"     ),
				dict(id=7, price=93,  size=5, meta="gdax"   ),
				dict(id=8, price=92,  size=4, neta="garbage" ),
	]
	
	OB = OrderBook(askOrders = AskOrders, bidOrders = BidOrders)
	print(OB)

#test()
