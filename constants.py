from enum import Enum

class Unit(Enum):
	ETH="ETH"
	LTC="LTC"
	BTC="BTC"
	USD="USD"
	EUR="EUR"
	GBP="GBP"

class OrderType(Enum):
	BID="Bid"
	OFFER="Offer"