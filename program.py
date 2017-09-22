import gdax, time, sys, threading
from GDAXClient import GDAXClient

# Import the configuration file
try:
	import config
except ImportError:
	sys.stderr.write("This script requires the use of a configuration file ./config.py\n")

def test():
	gClient = GDAXClient(products=["BTC-USD","ETH-USD"])
	gClient.start()
	time.sleep(1)
	gClient.close()

	# Prints the final state of gClient when the connection is closed
	print(gClient)

test()