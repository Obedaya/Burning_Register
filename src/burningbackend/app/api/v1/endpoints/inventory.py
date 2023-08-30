from burningbackend.app.models.inventory import Inventory, UpdateInventory

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()

@router.post("/", response_description="Inventory added to the database")
async def add_inventory(inventory: Inventory) -> dict:
    await inventory.create()
    inventory = await Inventory.find_one({"name": inventory.name})
    return {"message": "Inventory added successfully", "data": inventory}

@router.get("/", response_description="Inventory retrieved")
async def get_inventory() -> list[Inventory]:
    inventory = await Inventory.all().to_list()
    return inventory

@router.get("/{id}", response_description="Inventory retrieved")
async def get_inventory(id: str) -> Inventory:
    inventory = await Inventory.get(id)
    return inventory

# update sold amount
@router.put("/sold/{id}", response_description="Inventory data updated")
async def update_inventory_sold(id: str, amount: int) -> dict:
    inventory = await Inventory.get(id)
    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found"
        )
    inventory.amount_sold += amount
    inventory.amount -= amount
    await inventory.save()
    return {"message": "Inventory updated successfully", "data": inventory}


@router.put("/{id}", response_description="Inventory data updated")
async def update_inventory(id: str, req: UpdateInventory) -> dict:
    req = {k: v for k, v in req.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    inventory = await Inventory.get(id)
    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found"
        )
    updated_inventory = await inventory.update(update_query)
    return {"message": "Inventory updated successfully", "data": updated_inventory}

@router.delete("/{id}", response_description="Inventory deleted from the database")
async def delete_inventory(id: str) -> dict:
    inventory = await Inventory.get(id)
    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found!"
        )
    await inventory.delete()
    return {"message": "Inventory deleted successfully"}
