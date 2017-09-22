from constants import Unit, OrderType

class Quantity(object):
	def __init__(self, amount=0, units=Unit.USD):
		self.amount=amount
		self.units=units

class Order(object):
	def __init__(self, size=Quantity(), price=Quantity(), kind=OrderType.BID):
		self.size=size
		self.price=price
		self.kind=kind

		# Negative prices or quantities not supported
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
