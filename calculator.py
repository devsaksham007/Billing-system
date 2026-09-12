import math
import random
from datetime import datetime


class CalculatorError(Exception):
    """Base exception for calculator errors."""


class InvalidOperationError(CalculatorError):
    pass


class DivisionByZeroError(CalculatorError):
    pass


class InvalidNumberError(CalculatorError):
    pass


class Calculator:
    """Basic calculator that records information about each calculation."""

    def __init__(self, owner):
        if not isinstance(owner, str) or not owner.strip():
            raise InvalidNumberError("Calculator owner is required")

        self.owner = owner.strip()
        self.calculation_id = f"CAL-{random.randint(10000, 99999)}"
        self.last_result = None
        self.last_calculated_at = None

    def calculate(self, operation, first_number, second_number=None):
        first_number = self._validate_number(first_number)
        if second_number is not None:
            second_number = self._validate_number(second_number)

        if operation == "+":
            result = first_number + self._require_second_number(second_number)
        elif operation == "-":
            result = first_number - self._require_second_number(second_number)
        elif operation == "*":
            result = first_number * self._require_second_number(second_number)
        elif operation == "/":
            second_number = self._require_second_number(second_number)
            if second_number == 0:
                raise DivisionByZeroError("Cannot divide by zero")
            result = first_number / second_number
        else:
            raise InvalidOperationError(f"Unsupported operation: {operation}")

        return self._record_result(result)

    def _validate_number(self, value):
        if isinstance(value, bool):
            raise InvalidNumberError("Boolean values are not valid numbers")
        try:
            return float(value)
        except (TypeError, ValueError) as error:
            raise InvalidNumberError(f"Invalid number: {value}") from error

    def _require_second_number(self, value):
        if value is None:
            raise InvalidNumberError("This operation requires two numbers")
        return value

    def _record_result(self, result):
        self.last_result = result
        self.last_calculated_at = datetime.now()
        return result


class ScientificCalculator(Calculator):
    """Calculator with scientific operations using the same public interface."""

    def calculate(self, operation, first_number, second_number=None):
        first_number = self._validate_number(first_number)

        if operation == "sqrt":
            if first_number < 0:
                raise InvalidNumberError("Square root requires a non-negative number")
            return self._record_result(math.sqrt(first_number))

        if operation == "power":
            second_number = self._validate_number(second_number)
            return self._record_result(math.pow(first_number, second_number))

        return super().calculate(operation, first_number, second_number)


def run_demo():
    calculators = [Calculator("Alex"), ScientificCalculator("Jordan")]

    print(f"{calculators[0].owner}: {calculators[0].calculate('+', 10, 5):.2f}")
    print(f"{calculators[1].owner}: {calculators[1].calculate('sqrt', 81):.2f}")
    print(f"Calculation ID: {calculators[1].calculation_id}")
    print(f"Calculated at: {calculators[1].last_calculated_at:%Y-%m-%d %H:%M:%S}")

    try:
        calculators[0].calculate('/', 10, 0)
    except CalculatorError as error:
        print(f"Handled error: {error}")

    try:
        calculators[1].calculate('sqrt', -1)
    except CalculatorError as error:
        print(f"Handled error: {error}")


if __name__ == "__main__":
    run_demo()