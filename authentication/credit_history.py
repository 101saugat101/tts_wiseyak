from database import credit_store, credit_history, engine
from sqlalchemy import select, update
from sqlalchemy.orm import Session

def use_credit(user_id: str, credit_to_deduct: int):
    with Session(engine) as session:
        # Get user credit
        stmt = select(credit_store).where(credit_store.c.user_id == user_id)
        result = session.execute(stmt).mappings().first()

        if not result:
            raise Exception("User not found or no credit available.")

        current_remaining = result["remaining_credit"]

        if current_remaining < credit_to_deduct:
            raise Exception("Not enough credits.")

        new_remaining = current_remaining - credit_to_deduct

        # Update credit store
        session.execute(
            update(credit_store)
            .where(credit_store.c.user_id == user_id)
            .values(remaining_credit=new_remaining)
        )

        # Update latest credit_history
        stmt2 = select(credit_history).where(credit_history.c.user_id == user_id).order_by(credit_history.c.id.desc())
        history = session.execute(stmt2).mappings().first()

        if history:
            used_credit = history["used_credit"] + credit_to_deduct
            session.execute(
                update(credit_history)
                .where(credit_history.c.id == history["id"])
                .values(
                    used_credit=used_credit,
                    remaining_credit=new_remaining
                )
            )

        session.commit()
