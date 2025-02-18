import uuid
from fastapi import APIRouter, Body, Request

router = APIRouter()


# @router.post("/auth/generate-message")
# async def generate_message(wallet: str = Body(...)) -> str:
#     # Save the wallet to cache for reference later
#     set_cache_address(wallet)

#     # Generate a nonce
#     nonce = uuid.uuid4()

#     # Generate the message
#     return f"""
# Welcome! Sign this message to login to the site. This doesn't cost you
# anything and is free of any gas fees.

# Nonce:
# {nonce}.
#     """


# @router.post("/auth/signature")
# async def authorize_signature(request: Request) -> None:
#     public_key = request.headers.get("public_key", None)
#     signature = request.headers.get("signature", None)

#     try:
#         verify_signature(public_key, signature)
#     except:
#         return {"error": "Unauthorized"}

#     return {"message": public_key}
