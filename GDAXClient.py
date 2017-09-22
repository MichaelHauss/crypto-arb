import Order
from constants import Unit, OrderType
import gdax

class OrderBook(object):
	"""Represents an order book"""
	def __init__(self, sizeccy=Unit.BTC, priceccy=Unit.USD, bids=[], offers=[]):
		self.sizeccy=sizeccy
		self.priceccy=priceccy
		self.publicclient=gdax.PublicClient()

		# Get order book snapshot. <level> paramter described at https://docs.gdax.com/#get-product-order-book
		# Multiple instances of an order with the same price and size are coalesced
		raworderbook = self.publicclient.get_product_order_book(self.sizeccy.value + '-' + self.priceccy.value, level=2)
		self.bids = map(lambda bid: Order(
			size=Quantity(float(bid[1]) * float(bid[2]), self.sizeccy), 
			price=Quantity(float(bid[0]), self.priceccy), kind=OrderType.BID),
		raworderbook["bids"])
		self.offers = map(lambda offer: Order(
			size=Quantity(float(offer[1]) * float(offer[2]), self.sizeccy), 
			price=Quantity(float(offer[0]), self.priceccy), kind=OrderType.OFFER),
		raworderbook["asks"])

	# See https://docs.gdax.com/#real-time-order-book
	def update(self):
		return "Not Implemented"

	def __str__(self):

		# Helper function to print a list
		def format_list(l):
			formattedlist = ""
			for element in l:
				formattedlist += (element.__str__() + "\n")
			return formattedlist

		return "Size currency: %s\nPrice currency: %s\n\nBids:\n%s\n\nOffers:\n%s" % (
			self.sizeccy.value, self.priceccy.value, format_list(self.bids), format_list(self.offers))

def sanity_check():
	# testorder = Order(size=Quantity(100, Unit.BTC), price=Quantity(200, Unit.EUR), kind=OrderType.BID)
	# print(testorder)
	# print (testorder.get_dual())

	print(OrderBook())

sanity_check()
