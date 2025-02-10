from logging import getLogger
from eth_account.messages import encode_defunct

from web3 import Web3 as w3

logger = getLogger(__name__)


def verify_signature(address, signature, message):
    message_hash = encode_defunct(text=message)

    try:
        # Recover the public key from the signature
        public_key = w3.eth.account.recover_message(message_hash, signature=signature)
        # Convert the public key to an Ethereum address
        recovered_address = w3.to_checksum_address(
            w3.eth.account.public_key_to_address(public_key)
        )
        # Compare the recovered address with the provided address
        return address == recovered_address
    except Exception as e:
        logger.exception("Error verifying signature: %s", e)

    return False
