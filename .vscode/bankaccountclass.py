class InsufficientFundsError(Exception):
	pass


class Account:
	def __init__(self, owner, balance=0):
		self.owner = owner
		self.balance = balance

	def deposit(self, amount):
		self.balance += amount
		print(f"{self.owner} deposited {amount} -> balance {self.balance}")

	def withdraw(self, amount):
		if amount > self.balance:
			raise InsufficientFundsError(
				f"Insufficient funds: balance {self.balance}, requested {amount}"
			)
		self.balance -= amount

	def show(self):
		print(f"{self.owner}'s balance: {self.balance}")


account = Account("Arun", 1000)
account.deposit(500)

try:
	account.withdraw(2000)
except InsufficientFundsError as error:
	print(f"Error: {error}")
finally:
	print("Transaction finished")
