# from web3 import Web3
# from eth_account.messages import encode_defunct


# def verify_signature(address, signature, username):
#     username_hash = encode_defunct(text=username)

#     try:
#         # Recover the public key from the signature
#         address = Account.recover_message(username_hash, signature=signature)
#         # Convert the public key to an Ethereum address
#         recovered_address = Web3.toChecksumAddress(address)
#         # Compare the recovered address with the provided address
#         if address == recovered_address:
#             return True
#     except Exception as e:
#         return False

#     return False
