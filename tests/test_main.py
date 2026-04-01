import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create one client shared across all tests
client = TestClient(app)


# ─────────────────────────────────────────────
# HELPER
# Why: reduces repetition — every test needs
# to POST two numbers to an endpoint
# ─────────────────────────────────────────────

def post_operation(endpoint: str, a: float, b: float):
    """Send a POST request with a and b to the given endpoint."""
    return client.post(endpoint, json={"a": a, "b": b})


# ─────────────────────────────────────────────
# HEALTH & ROOT
# ─────────────────────────────────────────────

class TestHealthAndRoot:

    def test_health_endpoint_returns_200(self):
        # Arrange
        url = "/health"
        # Act
        response = client.get(url)
        # Assert
        assert response.status_code == 200

    def test_health_endpoint_returns_healthy_status(self):
        # Arrange
        url = "/health"
        # Act
        response = client.get(url)
        # Assert
        assert response.json()["status"] == "healthy"

    def test_root_returns_200(self):
        # Arrange
        url = "/"
        # Act
        response = client.get(url)
        # Assert
        assert response.status_code == 200

    def test_root_returns_html(self):
        # Arrange
        url = "/"
        # Act
        response = client.get(url)
        # Assert
        assert "text/html" in response.headers["content-type"]


# ─────────────────────────────────────────────
# ADD
# ─────────────────────────────────────────────

class TestAddEndpoint:

    def test_add_returns_200(self):
        # Arrange
        a, b = 2, 3
        # Act
        response = post_operation("/add", a, b)
        # Assert
        assert response.status_code == 200

    def test_add_correct_result(self):
        # Arrange
        a, b = 2, 3
        # Act
        response = post_operation("/add", a, b)
        # Assert
        assert response.json()["result"] == 5

    def test_add_negative_numbers(self):
        # Arrange
        a, b = -5, -3
        # Act
        response = post_operation("/add", a, b)
        # Assert
        assert response.json()["result"] == -8

    def test_add_floats(self):
        # Arrange
        a, b = 0.1, 0.2
        # Act
        response = post_operation("/add", a, b)
        # Assert
        assert response.json()["result"] == pytest.approx(0.3)

    def test_add_invalid_input_returns_400(self):
        # Arrange — sending a string instead of a number
        # Act
        response = client.post("/add", json={"a": "hello", "b": 2})
        # Assert
        assert response.status_code == 400


# ─────────────────────────────────────────────
# SUBTRACT
# ─────────────────────────────────────────────

class TestSubtractEndpoint:

    def test_subtract_returns_200(self):
        # Arrange
        a, b = 10, 4
        # Act
        response = post_operation("/subtract", a, b)
        # Assert
        assert response.status_code == 200

    def test_subtract_correct_result(self):
        # Arrange
        a, b = 10, 4
        # Act
        response = post_operation("/subtract", a, b)
        # Assert
        assert response.json()["result"] == 6

    def test_subtract_results_in_negative(self):
        # Arrange
        a, b = 3, 7
        # Act
        response = post_operation("/subtract", a, b)
        # Assert
        assert response.json()["result"] == -4

    def test_subtract_same_numbers_returns_zero(self):
        # Arrange
        a, b = 5, 5
        # Act
        response = post_operation("/subtract", a, b)
        # Assert
        assert response.json()["result"] == 0


# ─────────────────────────────────────────────
# MULTIPLY
# ─────────────────────────────────────────────

class TestMultiplyEndpoint:

    def test_multiply_returns_200(self):
        # Arrange
        a, b = 3, 4
        # Act
        response = post_operation("/multiply", a, b)
        # Assert
        assert response.status_code == 200

    def test_multiply_correct_result(self):
        # Arrange
        a, b = 6, 7
        # Act
        response = post_operation("/multiply", a, b)
        # Assert
        assert response.json()["result"] == 42

    def test_multiply_by_zero(self):
        # Arrange
        a, b = 999, 0
        # Act
        response = post_operation("/multiply", a, b)
        # Assert
        assert response.json()["result"] == 0

    def test_multiply_negative_numbers(self):
        # Arrange
        a, b = -3, 4
        # Act
        response = post_operation("/multiply", a, b)
        # Assert
        assert response.json()["result"] == -12


# ─────────────────────────────────────────────
# DIVIDE
# ─────────────────────────────────────────────

class TestDivideEndpoint:

    def test_divide_returns_200(self):
        # Arrange
        a, b = 10, 2
        # Act
        response = post_operation("/divide", a, b)
        # Assert
        assert response.status_code == 200

    def test_divide_correct_result(self):
        # Arrange
        a, b = 10, 2
        # Act
        response = post_operation("/divide", a, b)
        # Assert
        assert response.json()["result"] == 5.0

    def test_divide_returns_float(self):
        # Arrange
        a, b = 7, 2
        # Act
        response = post_operation("/divide", a, b)
        # Assert
        assert response.json()["result"] == pytest.approx(3.5)

    def test_divide_by_zero_returns_400(self):
        # Arrange
        a, b = 5, 0
        # Act
        response = post_operation("/divide", a, b)
        # Assert
        assert response.status_code == 400

    def test_divide_by_zero_returns_error_message(self):
        # Arrange
        a, b = 5, 0
        # Act
        response = post_operation("/divide", a, b)
        # Assert
        assert "zero" in response.json()["error"].lower()


# ─────────────────────────────────────────────
# POWER
# ─────────────────────────────────────────────

class TestPowerEndpoint:

    def test_power_returns_200(self):
        # Arrange
        a, b = 2, 8
        # Act
        response = post_operation("/power", a, b)
        # Assert
        assert response.status_code == 200

    def test_power_correct_result(self):
        # Arrange
        a, b = 2, 8
        # Act
        response = post_operation("/power", a, b)
        # Assert
        assert response.json()["result"] == 256

    def test_power_zero_exponent(self):
        # Arrange — anything to the power of 0 is 1
        a, b = 99, 0
        # Act
        response = post_operation("/power", a, b)
        # Assert
        assert response.json()["result"] == 1

    def test_power_fractional_exponent(self):
        # Arrange — square root of 16
        a, b = 16, 0.5
        # Act
        response = post_operation("/power", a, b)
        # Assert
        assert response.json()["result"] == pytest.approx(4.0)


# ─────────────────────────────────────────────
# MODULO
# ─────────────────────────────────────────────

class TestModuloEndpoint:

    def test_modulo_returns_200(self):
        # Arrange
        a, b = 10, 3
        # Act
        response = post_operation("/modulo", a, b)
        # Assert
        assert response.status_code == 200

    def test_modulo_correct_result(self):
        # Arrange
        a, b = 10, 3
        # Act
        response = post_operation("/modulo", a, b)
        # Assert
        assert response.json()["result"] == 1

    def test_modulo_even_division(self):
        # Arrange
        a, b = 10, 5
        # Act
        response = post_operation("/modulo", a, b)
        # Assert
        assert response.json()["result"] == 0

    def test_modulo_by_zero_returns_400(self):
        # Arrange
        a, b = 10, 0
        # Act
        response = post_operation("/modulo", a, b)
        # Assert
        assert response.status_code == 400

    def test_modulo_by_zero_returns_error_message(self):
        # Arrange
        a, b = 10, 0
        # Act
        response = post_operation("/modulo", a, b)
        # Assert
        assert "zero" in response.json()["error"].lower()