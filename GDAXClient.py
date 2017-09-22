import time, sys, threading, gdax
from OrderBook import OrderBook
from HalfOrderBook import HalfOrderBook
from constants import OrderType, Unit, Fees

class GDAXClient(gdax.WebsocketClient):
	"""Subscribes to and processes the GDAX feed"""
	def __init__(self, url="wss://ws-feed.gdax.com", products=None, message_type="subscribe",auth=False, \
		api_key="", api_secret="", api_passphrase="", client=gdax, orderbooks={}):

		self.url = url
		self.products = products
		self.type = message_type
		self.stop = False
		self.ws = None
		self.thread = None
		self.auth = auth
		self.api_key = api_key
		self.api_secret = api_secret
		self.api_passphrase = api_passphrase
		self.client = gdax.PublicClient()
		self.orderbooks = {}
		self.message_count = 0

		# Get an order book snapshot for each product pair. The <level> paramter is
		# described at https://docs.gdax.com/#get-product-order-book. Level 3
		# returns the full, non aggregated order book.
		for product in products:
			raworderbook = self.client.get_product_order_book(product, level=3) 
			self.orderbooks[product] = OrderBook(priceCcy=Unit(product.split("-")[1]), 
				sizeCcy=Unit(product.split("-")[0]), fee=Fees.GDAX,
				askOrders=map(lambda order: dict(id=order[2], price=float(order[0]), size=float(order[1])),
					raworderbook["asks"]),
				bidOrders=map(lambda order: dict(id=order[2], price=float(order[0]), size=float(order[1])),
					raworderbook["bids"]))

	def on_open(self):
		print("-- Hello! --")

	## TODO
	def on_message(self, msg):
		self.message_count = self.message_count + 1
	 
	def on_close(self):
		print("-- Goodbye! --")

	def __str__(self):
		return "Messages processed: " + str(self.message_count) + \
		"\n\nURL: " + self.url + "\n\nOrder Books:\n\n" + \
			"\n\n".join ([
				str(self.orderbooks[product]) for 
				product in self.products
				])

def test():

	# Print a snapshot of gClient
	gClient = GDAXClient(products=["BTC-USD","ETH-USD"])
	print(gClient)

#test()
