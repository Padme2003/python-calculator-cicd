"""
Módulo de calculadora simple para demostrar CI/CD
"""

class Calculator:
    """Clase que implementa operaciones matemáticas básicas"""
    
    def __init__(self):
        """Inicializa la calculadora"""
        self.result = 0
    
    def add(self, a, b):
        """
        Suma dos números
        
        Args:
            a (float): Primer número
            b (float): Segundo número
        
        Returns:
            float: Resultado de la suma
        """
        return a + b
    
    def subtract(self, a, b):
        """
        Resta dos números
        
        Args:
            a (float): Minuendo
            b (float): Sustraendo
        
        Returns:
            float: Resultado de la resta
        """
        return a - b
    
    def multiply(self, a, b):
        """
        Multiplica dos números
        
        Args:
            a (float): Primer factor
            b (float): Segundo factor
        
        Returns:
            float: Resultado de la multiplicación
        """
        return a * b
    
    def divide(self, a, b):
        """
        Divide dos números
        
        Args:
            a (float): Dividendo
            b (float): Divisor
        
        Returns:
            float: Resultado de la división
        
        Raises:
            ValueError: Si el divisor es cero
        """
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b
    
    def power(self, base, exponent):
        """
        Calcula la potencia de un número
        
        Args:
            base (float): Base
            exponent (float): Exponente
        
        Returns:
            float: Resultado de la potenciación
        """
        return base ** exponent
