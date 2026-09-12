class BankAccount:
    def __init__(self, account_holder, initial_balance=0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_holder = account_holder
        self.balance = float(initial_balance)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")

        self.balance -= amount

    def display_balance(self):
        print(f"{self.account_holder}'s balance: ${self.balance:.2f}")


if __name__ == "__main__":
    account = BankAccount("Alex", 1000)
    account.deposit(250)
    account.withdraw(100)
    account.display_balance()