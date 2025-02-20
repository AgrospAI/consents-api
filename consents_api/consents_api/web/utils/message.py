from pydantic import BaseModel


class Message(BaseModel):
    """Base class for extra response messages.

    :param BaseModel: base pydantic type.
    :type BaseModel: BaseModel
    """

    message: str
