# from fastapi import APIRouter, HTTPException, Request
# from database.database import database, features, user_credits, credit_usage, user_activity_logs
# from sqlalchemy import select, update, insert
# from datetime import datetime

# router = APIRouter()

# @router.get("/features/{feature_name}")
# async def use_feature(feature_name: str, request: Request):
#     user_id = request.query_params.get("user_id")

#     if not user_id:
#         raise HTTPException(status_code=400, detail="Missing user_id in query parameter")

#     # Step 1: Find the feature
#     query = select(features).where(features.c.name == feature_name)
#     feature = await database.fetch_one(query)

#     if not feature:
#         raise HTTPException(status_code=404, detail="Feature not found.")

#     is_free = feature["is_free"]
#     credit_cost = feature["credit_cost"]
#     feature_id = feature["id"]

#     # Step 2: If free, just log activity
#     if is_free:
#         await database.execute(
#             insert(user_activity_logs).values(
#                 user_id=user_id,
#                 activity_type="feature_use",
#                 feature_id=feature_id,
#                 details=f"Used free feature: {feature_name}",
#                 ip_address=request.client.host,
#                 user_agent=request.headers.get("user-agent"),
#                 created_at=datetime.utcnow()
#             )
#         )
#         return {"message": f"Free feature '{feature_name}' used successfully."}

#     # Step 3: For paid features, check user credit balance
#     user_wallet = await database.fetch_one(
#         select(user_credits).where(user_credits.c.user_id == user_id)
#     )

#     if not user_wallet:
#         raise HTTPException(status_code=404, detail="User wallet not found.")

#     if user_wallet["credits_balance"] < credit_cost:
#         raise HTTPException(status_code=402, detail="Insufficient credits.")

#     # Step 4: Deduct credits
#     new_balance = user_wallet["credits_balance"] - credit_cost
#     await database.execute(
#         update(user_credits)
#         .where(user_credits.c.user_id == user_id)
#         .values(credits_balance=new_balance, updated_at=datetime.utcnow())
#     )

#     # Step 5: Log credit usage
#     await database.execute(
#         insert(credit_usage).values(
#             user_id=user_id,
#             feature_id=feature_id,
#             credits_used=credit_cost,
#             created_at=datetime.utcnow()
#         )
#     )

#     # Step 6: Log activity
#     await database.execute(
#         insert(user_activity_logs).values(
#             user_id=user_id,
#             activity_type="feature_use",
#             feature_id=feature_id,
#             details=f"Used paid feature: {feature_name}",
#             ip_address=request.client.host,
#             user_agent=request.headers.get("user-agent"),
#             created_at=datetime.utcnow()
#         )
#     )

#     return {
#         "message": f"Paid feature '{feature_name}' used successfully.",
#         "credits_deducted": credit_cost,
#         "remaining_balance": new_balance
#     }

from fastapi import APIRouter, HTTPException, Request, Query
from database.database import database, features, user_credits, credit_usage, user_activity_logs
from sqlalchemy import select, update, insert
from datetime import datetime

router = APIRouter()

# Shared logic handler
async def handle_feature_use(user_id: str, feature_name: str, request: Request):
    # Step 1: Find the feature
    feature = await database.fetch_one(
        select(features).where(features.c.name == feature_name)
    )

    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found.")

    is_free = feature["is_free"]
    credit_cost = feature["credit_cost"]
    feature_id = feature["id"]

    # Step 2: If free
    if is_free:
    # Log into credit_usage even for free features
        await database.execute(
            insert(credit_usage).values(
                user_id=user_id,
                feature_id=feature_id,
                credits_used=0,
                created_at=datetime.utcnow()
            )
        )

        # Log into user_activity_logs
        await database.execute(
            insert(user_activity_logs).values(
                user_id=user_id,
                activity_type="feature_use",
                feature_id=feature_id,
                details=f"Used free feature: {feature_name}",
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent"),
                created_at=datetime.utcnow()
            )
        )

        return {"message": f"Free feature '{feature_name}' used successfully."}
    
    
    # Step 3: Paid feature — check and deduct credits
    wallet = await database.fetch_one(
        select(user_credits).where(user_credits.c.user_id == user_id)
    )

    if not wallet:
        raise HTTPException(status_code=404, detail="User wallet not found.")

    if wallet["credits_balance"] < credit_cost:
        raise HTTPException(status_code=402, detail="Insufficient credits.")

    new_balance = wallet["credits_balance"] - credit_cost

    await database.execute(
        update(user_credits)
        .where(user_credits.c.user_id == user_id)
        .values(credits_balance=new_balance, updated_at=datetime.utcnow())
    )

    await database.execute(
        insert(credit_usage).values(
            user_id=user_id,
            feature_id=feature_id,
            credits_used=credit_cost,
            created_at=datetime.utcnow()
        )
    )

    await database.execute(
        insert(user_activity_logs).values(
            user_id=user_id,
            activity_type="feature_use",
            feature_id=feature_id,
            details=f"Used paid feature: {feature_name}",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            created_at=datetime.utcnow()
        )
    )

    return {
        "message": f"Paid feature '{feature_name}' used successfully.",
        "credits_deducted": credit_cost,
        "remaining_balance": new_balance
    }


@router.get("/features/speech_to_text")
async def use_speech_to_text(user_id: str = Query(...), request: Request = None):
    return await handle_feature_use(user_id, "speech_to_text", request)

@router.get("/features/text_to_speech")
async def use_text_to_speech(user_id: str = Query(...), request: Request = None):
    return await handle_feature_use(user_id, "text_to_speech", request)

@router.get("/features/summarize")
async def use_summarize(user_id: str = Query(...), request: Request = None):
    return await handle_feature_use(user_id, "summarize", request)

@router.get("/features/diarization")
async def use_diarization(user_id: str = Query(...), request: Request = None):
    return await handle_feature_use(user_id, "diarization", request)

@router.get("/features/call_bot")
async def use_call_bot(user_id: str = Query(...), request: Request = None):
    return await handle_feature_use(user_id, "call_bot", request)

@router.get("/features/chatbot")
async def use_chatbot(user_id: str = Query(...), request: Request = None):
    return await handle_feature_use(user_id, "chatbot", request)
