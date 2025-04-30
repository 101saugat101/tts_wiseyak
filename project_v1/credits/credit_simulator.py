from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.database import database, user_credits, credit_purchases 
from sqlalchemy import select, update, insert
from datetime import datetime
import random
import string

router = APIRouter()

# Simulated request model
class CreditPurchaseRequest(BaseModel):
    user_id: str
    credit_amount: int

def generate_fake_reference():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

@router.post("/simulate_purchase")
async def simulate_purchase(data: CreditPurchaseRequest):
    # Check if user exists in user_credits table
    result = await database.fetch_one(
        select(user_credits).where(user_credits.c.user_id == data.user_id)
    )

    if not result:
        raise HTTPException(status_code=404, detail="User not found or has no wallet.")

    # Update user's credit balance
    new_balance = result["credits_balance"] + data.credit_amount

    await database.execute(
        update(user_credits)
        .where(user_credits.c.user_id == data.user_id)
        .values(
            credits_balance=new_balance,
            updated_at=datetime.utcnow()
        )
    )

    # Insert dummy credit purchase log
    await database.execute(
        insert(credit_purchases).values(
            user_id=data.user_id,
            credits_added=data.credit_amount,
            payment_provider=random.choice(["paypal", "stripe", "test_gateway"]),
            payment_reference=generate_fake_reference(),
            created_at=datetime.utcnow()
        )
    )

    return {
        "message": f"{data.credit_amount} credits added to user {data.user_id}.",
        "new_balance": new_balance
    }
