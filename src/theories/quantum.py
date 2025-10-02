from .base import BaseTheory
from src.core.implementations import Implementation

class QuantumTheory(BaseTheory):
    name = "Quantum Theory"

    def allows_implementation(self, impl: Implementation) -> bool:
        # quantum theory allows entanglement; allow everything by default
        return True
