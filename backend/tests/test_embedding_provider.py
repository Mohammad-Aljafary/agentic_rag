from agentic_rag.embeddings.provider import ONNXEmbeddingProvider


def test_onnx_provider_returns_correct_shape():
    provider = ONNXEmbeddingProvider()
    result = provider.embed(["hello world", "test"])
    assert len(result) == 2
    assert len(result[0]) == 384
    assert all(isinstance(v, float) for v in result[0])


def test_onnx_provider_deterministic():
    provider = ONNXEmbeddingProvider()
    a = provider.embed(["same text"])
    b = provider.embed(["same text"])
    assert a == b
