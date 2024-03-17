from fastapi import APIRouter

router = APIRouter()


@router.get("/beepbeep")
async def calculate_distances():
    return "done!"
