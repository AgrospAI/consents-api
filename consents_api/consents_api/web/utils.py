from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from web3 import Web3


def is_valid_signature(address: str, encoded_text: str) -> bool:
    """Checks whether the address signed the encoded text.

    Args:
        address (str): ETH address
        encoded_text (str): Encoded text to verify

    Returns:
        bool: If the passed text was signed by the signature
    """

    w3 = Web3(Web3.HTTPProvider(""))
    _message = encode_defunct(text=encoded_text)

    _address = w3.eth.account.recover_message(_message, signature=HexBytes(address))

    return address.lower() == _address.lower()
