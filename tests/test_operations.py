import pytest
from app.operations import add, subtract, multiply, divide, power, modulo


# ─────────────────────────────────────────────
# ADD
# ─────────────────────────────────────────────

class TestAdd:

    def test_add_two_positive_numbers(self):
        # Arrange
        a, b = 2, 3
        # Act
        result = add(a, b)
        # Assert
        assert result == 5

    def test_add_two_negative_numbers(self):
        # Arrange
        a, b = -2, -3
        # Act
        result = add(a, b)
        # Assert
        assert result == -5

    def test_add_positive_and_negative(self):
        # Arrange
        a, b = 10, -3
        # Act
        result = add(a, b)
        # Assert
        assert result == 7

    def test_add_with_zero(self):
        # Arrange
        a, b = 5, 0
        # Act
        result = add(a, b)
        # Assert
        assert result == 5

    def test_add_two_floats(self):
        # Arrange
        a, b = 0.1, 0.2
        # Act
        result = add(a, b)
        # Assert
        # NOTE: pytest.approx handles floating point precision issues
        # 0.1 + 0.2 in Python is 0.30000000000000004, not exactly 0.3
        assert result == pytest.approx(0.3)


# ─────────────────────────────────────────────
# SUBTRACT
# ─────────────────────────────────────────────

class TestSubtract:

    def test_subtract_two_positive_numbers(self):
        # Arrange
        a, b = 10, 4
        # Act
        result = subtract(a, b)
        # Assert
        assert result == 6

    def test_subtract_results_in_negative(self):
        # Arrange
        a, b = 3, 7
        # Act
        result = subtract(a, b)
        # Assert
        assert result == -4

    def test_subtract_same_numbers_returns_zero(self):
        # Arrange
        a, b = 5, 5
        # Act
        result = subtract(a, b)
        # Assert
        assert result == 0

    def test_subtract_with_zero(self):
        # Arrange
        a, b = 8, 0
        # Act
        result = subtract(a, b)
        # Assert
        assert result == 8


# ─────────────────────────────────────────────
# MULTIPLY
# ─────────────────────────────────────────────

class TestMultiply:

    def test_multiply_two_positive_numbers(self):
        # Arrange
        a, b = 3, 4
        # Act
        result = multiply(a, b)
        # Assert
        assert result == 12

    def test_multiply_by_zero(self):
        # Arrange
        a, b = 999, 0
        # Act
        result = multiply(a, b)
        # Assert
        assert result == 0

    def test_multiply_two_negative_numbers(self):
        # Arrange
        a, b = -3, -4
        # Act
        result = multiply(a, b)
        # Assert
        assert result == 12

    def test_multiply_positive_and_negative(self):
        # Arrange
        a, b = -3, 4
        # Act
        result = multiply(a, b)
        # Assert
        assert result == -12

    def test_multiply_floats(self):
        # Arrange
        a, b = 2.5, 4.0
        # Act
        result = multiply(a, b)
        # Assert
        assert result == pytest.approx(10.0)


# ─────────────────────────────────────────────
# DIVIDE
# ─────────────────────────────────────────────

class TestDivide:

    def test_divide_two_positive_numbers(self):
        # Arrange
        a, b = 10, 2
        # Act
        result = divide(a, b)
        # Assert
        assert result == 5.0

    def test_divide_returns_float(self):
        # Arrange
        a, b = 7, 2
        # Act
        result = divide(a, b)
        # Assert
        assert result == pytest.approx(3.5)

    def test_divide_negative_numerator(self):
        # Arrange
        a, b = -10, 2
        # Act
        result = divide(a, b)
        # Assert
        assert result == -5.0

    def test_divide_zero_numerator(self):
        # Arrange — dividing 0 by anything is valid, should return 0
        a, b = 0, 5
        # Act
        result = divide(a, b)
        # Assert
        assert result == 0.0

    def test_divide_by_zero_raises_value_error(self):
        # Arrange
        a, b = 5, 0
        # Act & Assert together — we expect this to raise an error
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(a, b)


# ─────────────────────────────────────────────
# POWER
# ─────────────────────────────────────────────

class TestPower:

    def test_power_basic(self):
        # Arrange
        a, b = 2, 10
        # Act
        result = power(a, b)
        # Assert
        assert result == 1024

    def test_power_zero_exponent(self):
        # Arrange — anything to the power of 0 is 1
        a, b = 99, 0
        # Act
        result = power(a, b)
        # Assert
        assert result == 1

    def test_power_one_exponent(self):
        # Arrange
        a, b = 5, 1
        # Act
        result = power(a, b)
        # Assert
        assert result == 5

    def test_power_fractional_exponent(self):
        # Arrange — 9^0.5 is the square root of 9 = 3
        a, b = 9, 0.5
        # Act
        result = power(a, b)
        # Assert
        assert result == pytest.approx(3.0)

    def test_power_negative_base(self):
        # Arrange
        a, b = -2, 3
        # Act
        result = power(a, b)
        # Assert
        assert result == -8


# ─────────────────────────────────────────────
# MODULO
# ─────────────────────────────────────────────

class TestModulo:

    def test_modulo_basic(self):
        # Arrange
        a, b = 10, 3
        # Act
        result = modulo(a, b)
        # Assert
        assert result == 1

    def test_modulo_even_division(self):
        # Arrange — 10 % 5 divides evenly, remainder is 0
        a, b = 10, 5
        # Act
        result = modulo(a, b)
        # Assert
        assert result == 0

    def test_modulo_smaller_dividend(self):
        # Arrange — 3 % 10, answer is 3 since 3 < 10
        a, b = 3, 10
        # Act
        result = modulo(a, b)
        # Assert
        assert result == 3

    def test_modulo_by_zero_raises_value_error(self):
        # Arrange
        a, b = 10, 0
        # Act & Assert
        with pytest.raises(ValueError, match="Cannot perform modulo by zero"):
            modulo(a, b)