from .base import BaseTheory
from src.core.implementations import Implementation

class BoxWorldTheory(BaseTheory):
    name = "BoxWorld (supernonlocal)"

    def allows_implementation(self, impl: Implementation) -> bool:
        # BoxWorld allows PR style components; accept everything
        return True
