from abc import ABC, abstractmethod
from typing import Optional
from src.core.implementations import Implementation

class BaseTheory(ABC):
    """Base class for theories; used to decide what implementations are allowed."""

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    def allows_implementation(self, impl: Implementation) -> bool:
        """
        By default assume any implementation is allowed.
        Subclasses may override to express restrictions (e.g., classical cannot have entangled state).
        """
        return True
