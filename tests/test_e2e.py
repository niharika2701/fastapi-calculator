
import pytest
from playwright.sync_api import Page, expect


# ─────────────────────────────────────────────
# FIXTURES
#
# WHY FIXTURES?
# A fixture is setup/teardown code shared across
# tests. The `live_server` fixture starts our
# FastAPI server once for all E2E tests, then
# stops it when done.
#
# `page` is provided automatically by
# pytest-playwright — it's a fresh browser tab.
# ─────────────────────────────────────────────

BASE_URL = "http://127.0.0.1:8000"


# ─────────────────────────────────────────────
# PAGE LOAD TESTS
# ─────────────────────────────────────────────

class TestPageLoad:

    def test_page_title_is_correct(self, page: Page):
        # Arrange
        url = BASE_URL
        # Act
        page.goto(url)
        # Assert
        expect(page).to_have_title("FastAPI Calculator")

    def test_logo_is_visible(self, page: Page):
        # Arrange
        page.goto(BASE_URL)
        # Act
        logo = page.locator(".logo")
        # Assert
        expect(logo).to_be_visible()

    def test_all_operation_buttons_present(self, page: Page):
        # Arrange
        page.goto(BASE_URL)
        # Act & Assert — check each operation button exists
        for op in ["add", "subtract", "multiply", "divide", "power", "modulo"]:
            btn = page.locator(f"[data-op='{op}']")
            expect(btn).to_be_visible()

    def test_input_fields_are_present(self, page: Page):
        # Arrange
        page.goto(BASE_URL)
        # Act & Assert
        expect(page.locator("#numA")).to_be_visible()
        expect(page.locator("#numB")).to_be_visible()

    def test_calculate_button_is_present(self, page: Page):
        # Arrange
        page.goto(BASE_URL)
        # Act
        btn = page.locator("#calcBtn")
        # Assert
        expect(btn).to_be_visible()

    def test_docs_link_is_present(self, page: Page):
        # Arrange
        page.goto(BASE_URL)
        # Act
        link = page.locator("a[href='/docs']")
        # Assert
        expect(link).to_be_visible()


# ─────────────────────────────────────────────
# CALCULATOR INTERACTION TESTS
# ─────────────────────────────────────────────

class TestCalculatorInteractions:

    def _calculate(self, page: Page, a: str, b: str, op: str):
        """
        Helper: fills inputs, selects operation, clicks calculate.
        Used by every interaction test to avoid repeating these steps.
        """
        page.goto(BASE_URL)
        page.fill("#numA", a)
        page.fill("#numB", b)
        page.click(f"[data-op='{op}']")
        page.click("#calcBtn")
        # Wait until result is no longer the loading state
        page.wait_for_function(
            "() => document.getElementById('result').textContent !== '...'"
        )

    def test_addition_shows_correct_result(self, page: Page):
        # Arrange
        a, b, op = "7", "3", "add"
        # Act
        self._calculate(page, a, b, op)
        # Assert
        expect(page.locator("#result")).to_have_text("10")

    def test_subtraction_shows_correct_result(self, page: Page):
        # Arrange
        a, b, op = "10", "4", "subtract"
        # Act
        self._calculate(page, a, b, op)
        # Assert
        expect(page.locator("#result")).to_have_text("6")

    def test_multiplication_shows_correct_result(self, page: Page):
        # Arrange
        a, b, op = "6", "7", "multiply"
        # Act
        self._calculate(page, a, b, op)
        # Assert
        expect(page.locator("#result")).to_have_text("42")

    def test_division_shows_correct_result(self, page: Page):
        # Arrange
        a, b, op = "15", "3", "divide"
        # Act
        self._calculate(page, a, b, op)
        # Assert
        expect(page.locator("#result")).to_have_text("5")

    def test_power_shows_correct_result(self, page: Page):
        # Arrange
        a, b, op = "2", "10", "power"
        # Act
        self._calculate(page, a, b, op)
        # Assert
        expect(page.locator("#result")).to_have_text("1024")

    def test_modulo_shows_correct_result(self, page: Page):
        # Arrange
        a, b, op = "10", "3", "modulo"
        # Act
        self._calculate(page, a, b, op)
        # Assert
        expect(page.locator("#result")).to_have_text("1")

    def test_expression_displayed_correctly(self, page: Page):
        # Arrange
        a, b, op = "5", "5", "add"
        # Act
        self._calculate(page, a, b, op)
        # Assert — expression area should show the calculation
        expr_text = page.locator("#expr").text_content()
        assert "5" in expr_text

    def test_divide_by_zero_shows_error(self, page: Page):
        # Arrange
        a, b, op = "10", "0", "divide"
        # Act
        self._calculate(page, a, b, op)
        # Assert — result should contain ERR
        result_text = page.locator("#result").text_content()
        assert "ERR" in result_text.upper()

    def test_enter_key_triggers_calculation(self, page: Page):
        # Arrange
        page.goto(BASE_URL)
        page.fill("#numA", "8")
        page.fill("#numB", "2")
        page.click("[data-op='add']")
        # Act — press Enter instead of clicking the button
        page.keyboard.press("Enter")
        page.wait_for_function(
            "() => document.getElementById('result').textContent !== '...'"
        )
        # Assert
        expect(page.locator("#result")).to_have_text("10")


# ─────────────────────────────────────────────
# HISTORY PANEL TESTS
# ─────────────────────────────────────────────

class TestHistoryPanel:

    def test_calculation_appears_in_history(self, page: Page):
        # Arrange
        page.goto(BASE_URL)
        page.fill("#numA", "3")
        page.fill("#numB", "3")
        page.click("[data-op='multiply']")
        # Act
        page.click("#calcBtn")
        page.wait_for_function(
            "() => document.getElementById('result').textContent !== '...'"
        )
        # Assert — a history item should now exist
        expect(page.locator(".history-item").first).to_be_visible()

    def test_clear_history_removes_items(self, page: Page):
        # Arrange — do a calculation first so history isn't empty
        page.goto(BASE_URL)
        page.fill("#numA", "1")
        page.fill("#numB", "1")
        page.click("#calcBtn")
        page.wait_for_function(
            "() => document.getElementById('result').textContent !== '...'"
        )
        # Act
        page.click("#clearHist")
        # Assert — empty message should reappear
        expect(page.locator(".history-empty")).to_be_visible()