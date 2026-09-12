import math
import random
from datetime import datetime


class BillingError(Exception):
    """Base exception for billing errors."""


class InvalidProductError(BillingError):
    pass


class InvalidBillError(BillingError):
    pass


class Product:
    """A product included on a bill."""

    def __init__(self, name, price, quantity):
        if not isinstance(name, str) or not name.strip():
            raise InvalidProductError("Product name is required")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise InvalidProductError("Price must be a number")
        if not math.isfinite(price) or price < 0:
            raise InvalidProductError("Price must be a finite, non-negative number")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise InvalidProductError("Quantity must be a positive whole number")

        self.name = name.strip()
        self.price = float(price)
        self.quantity = quantity

    def line_total(self):
        return self.price * self.quantity

    def display_row(self):
        return self.name, self.quantity, self.price, self.line_total()


class DiscountedProduct(Product):
    """A product that demonstrates inherited and overridden behavior."""

    def __init__(self, name, price, quantity, discount_percent):
        super().__init__(name, price, quantity)
        if not isinstance(discount_percent, (int, float)) or not 0 <= discount_percent <= 100:
            raise InvalidProductError("Discount must be between 0 and 100 percent")
        self.discount_percent = float(discount_percent)

    def line_total(self):
        discount = self.price * self.discount_percent / 100
        return (self.price - discount) * self.quantity

    def display_row(self):
        name, quantity, price, total = super().display_row()
        return f"{name} ({self.discount_percent:g}% off)", quantity, price, total


class Bill:
    """Collects products and calculates a tax-inclusive final total."""

    def __init__(self, customer_name, tax_rate=5):
        if not isinstance(customer_name, str) or not customer_name.strip():
            raise InvalidBillError("Customer name is required")
        if isinstance(tax_rate, bool) or not isinstance(tax_rate, (int, float)):
            raise InvalidBillError("Tax rate must be a number")
        if not 0 <= tax_rate <= 100:
            raise InvalidBillError("Tax rate must be between 0 and 100 percent")

        self.customer_name = customer_name.strip()
        self.tax_rate = float(tax_rate)
        self.bill_number = f"INV-{random.randint(10000, 99999)}"
        self.created_at = datetime.now()
        self.products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise InvalidBillError("Only Product objects can be added to a bill")
        self.products.append(product)

    def subtotal(self):
        return sum(product.line_total() for product in self.products)

    def tax(self):
        return self.subtotal() * self.tax_rate / 100

    def total(self):
        # Round up to the nearest cent so the displayed total is never short.
        return math.ceil((self.subtotal() + self.tax()) * 100) / 100

    def display(self):
        rows = [
            f"Invoice: {self.bill_number} | Date: {self.created_at:%Y-%m-%d %H:%M:%S}",
            f"Customer: {self.customer_name}",
            "-" * 68,
            f"{'Product':<30} {'Qty':>5} {'Price':>12} {'Total':>12}",
            "-" * 68,
        ]
        for product in self.products:
            name, quantity, price, line_total = product.display_row()
            rows.append(f"{name:<30} {quantity:>5} ${price:>11.2f} ${line_total:>11.2f}")

        rows.extend(
            [
                "-" * 68,
                f"{'Subtotal':>51} ${self.subtotal():>11.2f}",
                f"{'Tax (' + format(self.tax_rate, '.2f') + '%)':>51} ${self.tax():>11.2f}",
                f"{'FINAL TOTAL':>51} ${self.total():>11.2f}",
            ]
        )
        return "\n".join(rows)


def run_demo():
    bill = Bill("Alex", tax_rate=8.25)
    bill.add_product(Product("Wireless Mouse", 24.99, 2))
    bill.add_product(DiscountedProduct("USB-C Keyboard", 49.99, 1, 10))
    print(bill.display())

    try:
        bill.add_product(Product("Invalid quantity", 10, 0))
    except BillingError as error:
        print(f"\nHandled error: {error}")


if __name__ == "__main__":
    run_demo()