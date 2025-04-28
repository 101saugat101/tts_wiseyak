from database import credit_store, credit_history, engine
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

# def manually_add_credit(user_id: str, credit_amount: int):
#     with Session(engine) as session:
#         # Check if user already has a credit store record
#         stmt = select(credit_store).where(credit_store.c.user_id == user_id)
#         result = session.execute(stmt).first()

#         if result:
#             # User already has some credits - update existing record
#             current_remaining = result[credit_store.c.remaining_credit]
#             new_remaining = current_remaining + credit_amount
#             session.execute(
#                 update(credit_store)
#                 .where(credit_store.c.user_id == user_id)
#                 .values(
#                     purchased_credit=result[credit_store.c.purchased_credit] + credit_amount,
#                     remaining_credit=new_remaining
#                 )
#             )
#         else:
#             # First time adding credit for this user
#             session.execute(
#                 insert(credit_store).values(
#                     user_id=user_id,
#                     uuid=123456789,  # You can generate a proper UUID here
#                     purchased_credit=credit_amount,
#                     remaining_credit=credit_amount
#                 )
#             )

#         # Insert a new record in credit history
#         session.execute(
#             insert(credit_history).values(
#                 user_id=user_id,
#                 initial_credit=credit_amount,
#                 used_credit=0,
#                 remaining_credit=credit_amount,
#                 purchase_credit=credit_amount
#             )
#         )

#         session.commit()
#         print(f"Successfully added {credit_amount} credits to user {user_id}")



from database import credit_store, credit_history, engine
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

def manually_add_credit(user_id: str, credit_amount: int):
    with Session(engine) as session:
        # Select with mappings() to get dict-like result
        stmt = select(credit_store).where(credit_store.c.user_id == user_id)
        result = session.execute(stmt).mappings().first()

        if result:
            # Access by key name
            current_remaining = result["remaining_credit"]
            purchased_credit = result["purchased_credit"]

            new_remaining = current_remaining + credit_amount
            session.execute(
                update(credit_store)
                .where(credit_store.c.user_id == user_id)
                .values(
                    purchased_credit=purchased_credit + credit_amount,
                    remaining_credit=new_remaining
                )
            )
        else:
            # First time adding credit
            session.execute(
                insert(credit_store).values(
                    user_id=user_id,
                    uuid=123456789,  # You can later add real UUID
                    purchased_credit=credit_amount,
                    remaining_credit=credit_amount
                )
            )

        # Insert into credit history
        session.execute(
            insert(credit_history).values(
                user_id=user_id,
                initial_credit=credit_amount,
                used_credit=0,
                remaining_credit=credit_amount,
                purchase_credit=credit_amount
            )
        )

        session.commit()
        print(f"Successfully added {credit_amount} credits to user {user_id}")
