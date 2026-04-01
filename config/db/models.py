from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", String(50), primary_key=True),
    Column("name", String(100)),
    Column("email", String(150), unique=True),
    Column("age", Integer),
)

address = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String(50), ForeignKey("users.id")),
    Column("street", String(200)),
    Column("city", String(100)),
    Column("country", String(100)),
    Column("activity_location", String(100)),
)

activity = Table(
    "activity",
    metadata,
    Column("id", String(50), primary_key=True),
    Column("user_id", String(50), ForeignKey("users.id")),
    Column("action", Text),
    Column("timestamp", TIMESTAMP(timezone=True)),
    Column("ip_address", String(50)),
)
