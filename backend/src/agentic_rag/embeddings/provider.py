from __future__ import annotations

from abc import ABC, abstractmethod

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class ONNXEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self._ef = DefaultEmbeddingFunction()

    def embed(self, texts: list[str]) -> list[list[float]]:
        result = self._ef(texts)
        return [[float(v) for v in row] for row in result]
