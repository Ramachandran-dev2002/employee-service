class InsufficientFundsError(Exception):
	pass


class Account:
	def __init__(self, balance):
		self.balance = balance

	def withdraw(self, amount):
		if amount > self.balance:
			raise InsufficientFundsError(
				f"Insufficient funds: balance {self.balance}, requested {amount}"
			)
		self.balance -= amount


class SavingsAccount(Account):
	def __init__(self, balance):
		super().__init__(balance)
		self.min_balance = 500

	def withdraw(self, amount):
		if self.balance - amount < self.min_balance:
			raise InsufficientFundsError(
				f"Insufficient funds: balance {self.balance}, requested {amount}"
			)
		self.balance -= amount


priya = SavingsAccount(1500)

try:
	priya.withdraw(1200)
except InsufficientFundsError as error:
	print(f"Error: {error}")

priya.withdraw(800)
print(f"Priya withdrew 800 -> balance {priya.balance}")
print(isinstance(priya, Account))  # True: SavingsAccount inherits from Account.
