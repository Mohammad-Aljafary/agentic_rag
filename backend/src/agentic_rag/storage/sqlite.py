import sqlAlchemy as sa


engine = sa.create_engine("sqlite:///my_database.db")

metadata = sa.MetaData()

sources = sa.Table(
    "sources",
    metadata,
    sa.Column("source_id", sa.String, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("source_type", sa.String),
    sa.Column("uri", sa.String),
    sa.Column("metadata_json", sa.JSON),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
)

chunks = sa.Table(
    "chunks",
    metadata,
    sa.Column("chunk_id", sa.String, primary_key=True),
    sa.Column("source_id", sa.String, sa.ForeignKey("sources.source_id")),
    sa.Column("text", sa.Text),
    sa.Column("chunk_index", sa.Integer),
    sa.Column("metadata_json", sa.JSON),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
)