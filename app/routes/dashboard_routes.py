from fastapi import APIRouter, Depends
from app.database import records_collection
from app.middleware.auth_middleware import require_role

router = APIRouter()


@router.get("/summary")
async def get_summary(user=Depends(require_role(["admin", "analyst"]))):
    pipeline = [
        {"$match": {"is_deleted": False}},
        {
            "$group": {
                "_id": "$type",
                "total": {"$sum": "$amount"}
            }
        }
    ]

    result = await records_collection.aggregate(pipeline).to_list(10)

    income = 0
    expense = 0

    for r in result:
        if r["_id"] == "income":
            income = r["total"]
        elif r["_id"] == "expense":
            expense = r["total"]

    return {
        "totalIncome": income,
        "totalExpense": expense,
        "netBalance": income - expense
    }


@router.get("/trends")
async def monthly_trends(user=Depends(require_role(["admin", "analyst"]))):
    pipeline = [
        {"$match": {"is_deleted": False}},
        {
            "$group": {
                "_id": {
                    "month": {"$month": "$date"},
                    "type": "$type"
                },
                "total": {"$sum": "$amount"}
            }
        }
    ]

    result = await records_collection.aggregate(pipeline).to_list(100)

    month_map = {}

    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    for r in result:
        month = r["_id"]["month"]
        type_ = r["_id"]["type"]
        total = r["total"]

        if month not in month_map:
            month_map[month] = {
                "month": month_names[month - 1],
                "income": 0,
                "expense": 0
            }

        month_map[month][type_] = total

    sorted_data = sorted(
        month_map.values(),
        key=lambda x: month_names.index(x["month"])
    )

    return sorted_data