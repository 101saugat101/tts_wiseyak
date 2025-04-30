from database import credit_store, credit_history, engine
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

def use_credit(user_id: str, credit_to_deduct: int):
    with Session(engine) as session:
        # Get user's credit balance
        stmt = select(credit_store).where(credit_store.c.user_id == user_id)
        result = session.execute(stmt).mappings().first()

        if not result:
            raise Exception("User not found or no credit available.")

        current_remaining = result["remaining_credit"]

        if current_remaining < credit_to_deduct:
            raise Exception("Not enough credits.")

        new_remaining = current_remaining - credit_to_deduct

        # Update credit_store table
        session.execute(
            update(credit_store)
            .where(credit_store.c.user_id == user_id)
            .values(remaining_credit=new_remaining)
        )

        # INSERT new record in credit_history table instead of update
        session.execute(
            insert(credit_history).values(
                user_id=user_id,
                initial_credit=current_remaining,   # previous balance
                used_credit=credit_to_deduct,        # how much deducted
                remaining_credit=new_remaining,     # after deduction
                purchase_credit=0                    # 0 because it's usage, not purchase
            )
        )

        session.commit()
