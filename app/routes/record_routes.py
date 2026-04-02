from fastapi import APIRouter, Depends, Query
from app.database import records_collection
from app.middleware.auth_middleware import require_role
from app.schemas.record_schema import RecordCreate

router = APIRouter()

@router.post("/")
async def create_record(record: RecordCreate, user=Depends(require_role(["admin"]))):
    data = record.dict()
    data["created_by"] = user["id"]
    data["is_deleted"] = False

    await records_collection.insert_one(data)
    return {"message": "Record created"}

@router.get("/")
async def get_records(
    type: str = Query(None),
    category: str = Query(None),
    user=Depends(require_role(["admin", "analyst"]))
):
    query = {"is_deleted": False}

    if type:
        query["type"] = type
    if category:
        query["category"] = category

    records = []
    async for r in records_collection.find(query):
        r["_id"] = str(r["_id"])
        records.append(r)

    return records

@router.delete("/{record_id}")
async def delete_record(record_id: str, user=Depends(require_role(["admin"]))):
    await records_collection.update_one(
        {"_id": record_id},
        {"$set": {"is_deleted": True}}
    )
    return {"message": "Record deleted"}