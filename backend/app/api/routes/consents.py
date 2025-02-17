from fastapi import APIRouter

router = APIRouter(tags=["consents"])


@router.get("/consents/")
def get_consents():
    return {"consents": "consents"}
