# from sqlalchemy import (
#     create_engine,
#     MetaData,
#     Table,
#     Column,
#     String,
#     Integer,
#     Boolean,
#     BigInteger,
#     Text,
#     DateTime,
#     ForeignKey,
#     func,
# )
# from sqlalchemy.dialects.postgresql import UUID
# import uuid

# # Database URL
# DATABASE_URL = "postgresql://postgres:heheboii420@localhost/SAAS"

# # Connect to database
# engine = create_engine(DATABASE_URL)
# metadata = MetaData()

# # 1. Users Table
# users = Table(
#     "users",
#     metadata,
#     Column("id", String, primary_key=True),  # Google OAuth ID
#     Column("email", String, unique=True, nullable=False),
#     Column("name", String),
#     Column("picture", String),
#     Column("created_at", DateTime(timezone=True), server_default=func.now()),
#     Column("last_login_at", DateTime(timezone=True)),
# )

# # 2. User Credits Table (current balance)
# user_credits = Table(
#     "user_credits",
#     metadata,
#     Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
#     Column("credits_balance", BigInteger, nullable=False, default=0),
#     Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
# )

# # 3. Features Table
# features = Table(
#     "features",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("name", String, nullable=False),
#     Column("description", Text),
#     Column("is_free", Boolean, default=False),
#     Column("credit_cost", Integer, default=0),
# )

# # 4. Credit Purchases Table
# credit_purchases = Table(
#     "credit_purchases",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE")),
#     Column("credits_added", Integer, nullable=False),
#     Column("payment_provider", String),
#     Column("payment_reference", String),
#     Column("created_at", DateTime(timezone=True), server_default=func.now()),
# )

# # 5. Credit Usage Table
# credit_usage = Table(
#     "credit_usage",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE")),
#     Column("feature_id", Integer, ForeignKey("features.id", ondelete="SET NULL")),
#     Column("credits_used", Integer, nullable=False),
#     Column("created_at", DateTime(timezone=True), server_default=func.now()),
# )

# # 6. User Activity Logs Table
# user_activity_logs = Table(
#     "user_activity_logs",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE")),
#     Column("activity_type", String, nullable=False),
#     Column("feature_id", Integer, ForeignKey("features.id", ondelete="SET NULL"), nullable=True),
#     Column("details", Text),
#     Column("ip_address", String),
#     Column("user_agent", Text),
#     Column("created_at", DateTime(timezone=True), server_default=func.now()),
# )

# # Run this file to create all tables
# if __name__ == "__main__":
#     metadata.create_all(engine)
#     print("✅ All tables created successfully in the SAAS database.")


from sqlalchemy import (
    create_engine, MetaData, Table, Column, String, Integer, Boolean, BigInteger,
    Text, DateTime, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID
from databases import Database

# SQLAlchemy setup
DATABASE_URL = "postgresql://postgres:heheboii420@localhost/SAAS"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Users table
users = Table(
    "users", metadata,
    Column("id", String, primary_key=True),
    Column("email", String),
    Column("name", String),
    Column("picture", String),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("last_login_at", DateTime(timezone=True))
)

# User credit balance table
user_credits = Table(
    "user_credits", metadata,
    Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("credits_balance", BigInteger, nullable=False, default=0),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
)

# Credit purchases
credit_purchases = Table(
    "credit_purchases", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE")),
    Column("credits_added", Integer, nullable=False),
    Column("payment_provider", String),
    Column("payment_reference", String),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)


# 3. Features Table
features = Table(
    "features",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("description", Text),
    Column("is_free", Boolean, default=False),
    Column("credit_cost", Integer, default=0),
)


# 6. User Activity Logs Table
user_activity_logs = Table(
    "user_activity_logs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE")),
    Column("activity_type", String, nullable=False),
    Column("feature_id", Integer, ForeignKey("features.id", ondelete="SET NULL"), nullable=True),
    Column("details", Text),
    Column("ip_address", String),
    Column("user_agent", Text),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

# 5. Credit Usage Table
credit_usage = Table(
    "credit_usage",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String, ForeignKey("users.id", ondelete="CASCADE")),
    Column("feature_id", Integer, ForeignKey("features.id", ondelete="SET NULL")),
    Column("credits_used", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)


# Add more tables as needed...

# Create tables
metadata.create_all(engine)

# ✅ This is what you're missing!
database = Database(DATABASE_URL)
