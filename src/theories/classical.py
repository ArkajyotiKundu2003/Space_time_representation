from .base import BaseTheory
from src.core.implementations import Implementation

class ClassicalTheory(BaseTheory):
    name = "Classical Theory"

    def allows_implementation(self, impl: Implementation) -> bool:
        # very simple rule: classical theory forbids components with metadata 'quantum'
        for c in impl.components:
            if c.metadata and c.metadata.get("quantum", False):
                return False
        return True
