from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime

from config.db import db

collection = db.orders


class Order(BaseModel):
    products: List[dict]
    total: str


router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("/")
async def get_orders():
    orders = await collection.find().to_list(None)
    if not orders:
        raise HTTPException(status_code=404, detail="No Orders Found")
    return orders


@router.post("/", status_code=201)
async def add_order(new_order: Order):
    order = {
        "_id": str(uuid4()),
        "products": new_order.products,
        "date_created": str(datetime.now()),
        "total": new_order.total,
    }
    try:
        await collection.insert_one(order)
        return {"detail": "Order Created Successfully"}
    except Exception as e:
        raise HTTPException(status_code=500) from e


@router.put("/{order_id}", status_code=201)
async def update_order(order_id: str, updated_order: Order):
    order = {
        "products": updated_order.products,
        "date_created": str(datetime.now()),
        "total": updated_order.total,
    }
    result = await collection.update_one({"_id": order_id}, {"$set": order})
    if not result.modified_count:
        raise HTTPException(
            status_code=404, detail=f"Order with ID: {order_id} was not updated"
        )
    return {"detail": "Order Updated Successfully"}


@router.delete("/", status_code=202)
async def clear_orders():
    try:
        result = await collection.delete_many({})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="No orders found to delete")
        return {"detail": f"Successfully cleared {result.deleted_count} orders"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
