from fastapi import APIRouter, HTTPException
from credit_history import use_credit

router = APIRouter()

@router.get("/api1")
def api1(user_id: str):
    try:
        use_credit(user_id, 2)
        return {"message": "Successfully deducted 2 credits."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api2")
def api2(user_id: str):
    try:
        use_credit(user_id, 4)
        return {"message": "Successfully deducted 4 credits."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
