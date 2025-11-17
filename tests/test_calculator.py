"""
Pruebas unitarias para el módulo calculator
"""

import pytest
from calculator import Calculator


class TestCalculator:
    """Clase de pruebas para Calculator"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.calc = Calculator()

    def test_add(self):
        """Prueba la función de suma"""
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0, 0) == 0
        assert self.calc.add(1.5, 2.5) == 4.0

    def test_subtract(self):
        """Prueba la función de resta"""
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(0, 5) == -5
        assert self.calc.subtract(-3, -3) == 0
        assert self.calc.subtract(10.5, 0.5) == 10.0

    def test_multiply(self):
        """Prueba la función de multiplicación"""
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(0, 100) == 0
        assert self.calc.multiply(-2, 3) == -6
        assert self.calc.multiply(2.5, 2) == 5.0

    def test_divide(self):
        """Prueba la función de división"""
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(7, 2) == 3.5
        assert self.calc.divide(-10, 2) == -5
        assert self.calc.divide(1, 3) == pytest.approx(0.3333, 0.001)

    def test_divide_by_zero(self):
        """Prueba que la división por cero lance una excepción"""
        with pytest.raises(ValueError) as excinfo:
            self.calc.divide(10, 0)
        assert "No se puede dividir por cero" in str(excinfo.value)

    def test_power(self):
        """Prueba la función de potenciación"""
        assert self.calc.power(2, 3) == 8
        assert self.calc.power(5, 0) == 1
        assert self.calc.power(10, -1) == 0.1
        assert self.calc.power(9, 0.5) == 3


class TestCalculatorIntegration:
    """Pruebas de integración para operaciones complejas"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.calc = Calculator()

    def test_complex_operation(self):
        """Prueba una operación compleja combinando varias funciones"""
        # (10 + 5) * 2 - 8 / 4
        result1 = self.calc.add(10, 5)  # 15
        result2 = self.calc.multiply(result1, 2)  # 30
        result3 = self.calc.divide(8, 4)  # 2
        final = self.calc.subtract(result2, result3)  # 28
        assert final == 28

    def test_chain_operations(self):
        """Prueba encadenamiento de operaciones"""
        # 2^3 + 10 - 5 * 2
        power_result = self.calc.power(2, 3)  # 8
        sum_result = self.calc.add(power_result, 10)  # 18
        mult_result = self.calc.multiply(5, 2)  # 10
        final = self.calc.subtract(sum_result, mult_result)  # 8
        assert final == 8


# Pruebas parametrizadas
@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, -1, -2),
        (100, 200, 300),
        (1.5, 2.5, 4.0),
    ],
)
def test_add_parametrized(a, b, expected):
    """Prueba parametrizada para la suma"""
    calc = Calculator()
    assert calc.add(a, b) == expected
