import pytest
from httpx import ASGITransport, AsyncClient

from agentic_rag.api import create_app


@pytest.mark.anyio
async def test_health_endpoint_reports_ready_service():
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "agentic-rag",
        "version": "0.1.0",
    }
