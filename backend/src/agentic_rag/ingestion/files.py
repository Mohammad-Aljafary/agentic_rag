"""Local file discovery and reading for ingestion."""

from __future__ import annotations

import hashlib
from pathlib import Path

from agentic_rag.models.rag import DocumentSource, SourceType


SUPPORTED_EXTENSIONS: dict[str, SourceType] = {
    ".txt": SourceType.text,
    ".md": SourceType.markdown,
}


def discover_ingestable_files(path: str | Path) -> list[Path]:
    """Return supported local files in deterministic path order."""
    root = Path(path)

    if root.is_file():
        if root.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [root]
        return []

    if not root.exists():
        return []

    files = [
        candidate
        for candidate in root.rglob("*")
        if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files, key=lambda file_path: str(file_path))


def read_local_document(file_path: str | Path) -> tuple[DocumentSource, str]:
    """Read a supported local document and build stable source metadata."""
    path = Path(file_path)
    content_bytes = path.read_bytes()
    text = content_bytes.decode("utf-8")
    content_hash = hashlib.sha256(content_bytes).hexdigest()
    resolved_path = path.resolve()
    stat = path.stat()

    source = DocumentSource(
        source_id=f"doc_{content_hash[:16]}",
        title=path.stem,
        source_type=SUPPORTED_EXTENSIONS.get(path.suffix.lower(), SourceType.unknown),
        uri=str(resolved_path),
        metadata={
            "source_path": str(resolved_path),
            "content_hash": content_hash,
            "file_size": stat.st_size,
            "modified_at": stat.st_mtime,
        },
    )
    return source, text

def add_source_to_database(source: DocumentSource, db_session) -> None:
    """Add a document source to the database."""
    db_session.add(source)
    db_session.commit()
