# from sqlalchemy import Table, Column, String, BigInteger, MetaData, ForeignKey, create_engine

# # Your database URL
# DATABASE_URL = "postgresql://postgres:heheboii420@localhost/oauth2"




# engine = create_engine(DATABASE_URL)
# metadata = MetaData()

# # Users table
# users = Table(
#     "users",
#     metadata,
#     Column("id", String, primary_key=True),
#     Column("email", String),
#     Column("name", String),
#     Column("picture", String),
# )

# # Credit store
# credit_store = Table(
#     "credit_store",
#     metadata,
#     Column("user_id", String, ForeignKey("users.id"), primary_key=True),
#     Column("uuid", BigInteger),
#     Column("purchased_credit", BigInteger),
    
# )

# # Credit history
# credit_history = Table(
#     "credit_history",
#     metadata,
#     Column("user_id", String, ForeignKey("users.id"), primary_key=True),
#     Column("initial_credit", BigInteger),
#     Column("used_credit", BigInteger),
#     Column("remaining_credit", BigInteger),
# )

# # Run when executed directly
# if __name__ == "__main__":
#     metadata.create_all(engine)
#     print("✅ Tables created successfully!")



from sqlalchemy import Table, Column, String, BigInteger, MetaData, ForeignKey, create_engine, Integer

# Your database URL
DATABASE_URL = "postgresql://postgres:heheboii420@localhost/oauth2"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Users table
users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("email", String),
    Column("name", String),
    Column("picture", String),
)

# Credit store (current balance)
credit_store = Table(
    "credit_store",
    metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("uuid", BigInteger),
    Column("purchased_credit", BigInteger),
    Column("remaining_credit", BigInteger),  # Add remaining_credit to easily update balance
)

# Credit purchase history
credit_history = Table(
    "credit_history",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("user_id", String, ForeignKey("users.id")),
    Column("initial_credit", BigInteger),
    Column("used_credit", BigInteger),
    Column("remaining_credit", BigInteger),
    Column("purchase_credit", BigInteger),
)


# Create tables if they don't exist
if __name__ == "__main__":
    metadata.create_all(engine)