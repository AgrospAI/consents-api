from fastapi import APIRouter

router = APIRouter(
    prefix="/consents",
    tags=["consents"],
    responses={404: {"description": "Not found"}},
)

@router.get("/me")
async def read_consents():
    return []

