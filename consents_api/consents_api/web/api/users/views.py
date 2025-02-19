import uuid

from fastapi import APIRouter, Body, Request

from consents_api.web.api.users.schema import UserDTO

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{address}")
async def get_user(address: str) -> UserDTO:
    """Retrieves user data from the given address.

    :param address: address of the user.
    :type address: str
    :return:
    :rtype: str
    """
    return UserDTO(
        public_key=address,
        consents=[],
    )


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
