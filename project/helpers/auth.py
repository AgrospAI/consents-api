from eth_utils import to_checksum_address


def build_siwe_message(
    *,
    domain: str,
    address: str,
    statement: str,
    uri: str,
    version: str,
    chain_id: int,
    nonce: str,
    issued_at_iso: str,
    expires_at_iso: str,
) -> str:
    """Constructs a human-readable SIWE-like message to keep consistency"""

    lines = [
        f"{domain} wants you to sign in with your Ethereum account:",
        f"{to_checksum_address(address)}",
        "",
        statement.strip(),
        "",
        f"URI: {uri}",
        f"Version: {version}",
        f"Chain ID: {chain_id}",
        f"Nonce: {nonce}",
        f"Issued At: {issued_at_iso}",
        f"Expiration Time: {expires_at_iso}",
    ]

    return "\n".join(lines).strip()
