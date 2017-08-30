from constants import Unit, OrderType
import gdax

class Quantity(object):
	def __init__(self, amount=0, units=Unit.USD):
		self.amount=amount
		self.units=units

class Order(object):
	def __init__(self, size=Quantity(), price=Quantity(), kind=OrderType.BID):
		self.size=size
		self.price=price
		self.kind=kind

		# We do not currently handle negative prices or quantities
		assert self.size.amount >= 0, "Order size must be greater than or equal to 0"
		assert self.price.amount >= 0, "Order price must be greater than or equal to 0"


	def get_dual(self):
		"""Describe the order with respect to the inverse kind (bid / offer)"""
		dualprice = Quantity(amount=1.0/self.price.amount, units=self.size.units)
		dualsize = Quantity(amount=self.price.amount * self.size.amount, units=self.price.units)
		dualkind = OrderType.BID if self.kind == OrderType.OFFER else OrderType.OFFER
		return Order(dualsize, dualprice, dualkind)

	def __str__(self):
		return "%s for %f %s @ %f %s / %s" % (self.kind.value, self.size.amount, \
			self.size.units.value, abs(self.price.amount), self.price.units.value, self.size.units.value)

	# TODO 
	def execute():
		return "Not Implemented"

class OrderBook(object):
	"""Represents an order book"""
	def __init__(self, sizeccy=Unit.BTC, priceccy=Unit.USD, bids=[], offers=[]):
		self.sizeccy=sizeccy
		self.priceccy=priceccy
		self.publicclient=gdax.PublicClient()

		# Get order book snapshot. <level> paramter described at https://docs.gdax.com/#get-product-order-book
		raworderbook = self.publicclient.get_product_order_book(self.sizeccy.value + '-' + self.priceccy.value, level=2)
		print(raworderbook)

	# See https://docs.gdax.com/#real-time-order-book
	def update(self):
		return "Not Implemented"

	def __str__(self):
		return "Not Implemented"

def sanity_check():
	# testorder = Order(size=Quantity(100, Unit.BTC), price=Quantity(200, Unit.EUR), kind=OrderType.BID)
	# print(testorder)
	# print (testorder.get_dual())

	OrderBook()

sanity_check()


