import gdax, time, sys, threading

# Import the configuration file
try:
	import config
except ImportError:
	sys.stderr.write("This script requires the use of a configuration file ./config.py\n")

# Websocket client
class myWebsocketClient(gdax.WebsocketClient):

	def __init__(self, url="wss://ws-feed.gdax.com", products=None, message_type="subscribe",auth=False, api_key="", api_secret="", api_passphrase="", client=gdax, orderbooks=None):
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

		# TODO
		self.orderbooks = map(lambda product: product + "-order-book", self.products)

	def on_open(self):
		print("Session started with orderbooks: {}".format(self.orderbooks))

	def on_message(self, msg):
		print("Message recived")
		
		# Update the order book
	 
	def on_close(self):
		print("-- Goodbye! --")

wsClient = myWebsocketClient(products=["LTC-USD", "ETH-USD"])
wsClient.start()
time.sleep(5)
wsClient.close()