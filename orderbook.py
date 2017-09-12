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

		# these will need to be stored in an ordered data structure...
		# ...do people actually use Min/Max heaps?
		# self.bids=[]
		# self.asks=[]

		# Get order book snapshot. <level> paramter described at https://docs.gdax.com/#get-product-order-book
		raworderbook = self.publicclient.get_product_order_book(self.sizeccy.value + '-' + self.priceccy.value, level=2)
		print(raworderbook)

		# Here we would populate the bids and offers. To start let's use the level2
		# websocket channel, which is apparently too slow but no dropped messages.
		# Can update to level3 once we've handled the main cases if necessary

	# See https://docs.gdax.com/#real-time-order-book
	def update(self):
		return "Not Implemented"
		# I think the channel should exist outside of the OrderBook, i.e. we will
		# pass in a message here and handle it (see Book.py in the Pierre Git)

	def __str__(self):
		return "Not Implemented"

	# For the given order book, what would be the wtd avg price to sell "size"?
	# Alternatively could make it the total price (i.e. I'm indifferent whether we
	# multiply by size or not)
	def bidPrice(self,size=Quantity()):
		return Quantity()

	# What quantity could I sell at "price"?
	def bidAmount(self,price=Quantity())
		# iterate through the bids  (or offers if I'm trying to sell the weaker 
		# currency, i.e. sell USD on a BTCUSD book) from smallest to largest, summing the 
		# sizes until you hit price (or 1/price if weaker currency)
		return Quantity()

	# What is the best bid (agnostic of bid size)
	def bestBid(self):
		return Quantity()

	# would then duplicate these methods for Offers
	# The last methods we would want are ways to actually execute Orders... we'll have
	# to think about if that will be a property of the book... current framework where
	# we pass in messages would suggest that the OrderBook should be used to generate
	# an Order which would then be executed


def sanity_check():
	# testorder = Order(size=Quantity(100, Unit.BTC), price=Quantity(200, Unit.EUR), kind=OrderType.BID)
	# print(testorder)
	# print (testorder.get_dual())

	OrderBook()

sanity_check()


