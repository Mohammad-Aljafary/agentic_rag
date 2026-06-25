from fastapi import FastAPI

from agentic_rag import __version__


def create_app() -> FastAPI:
    app = FastAPI(title="Agentic RAG", version=__version__)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {
            "status": "ok",
            "service": "agentic-rag",
            "version": __version__,
        }

    return app


app = create_app()
