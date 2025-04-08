from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class AquariusService:
    url: str = "https://aquarius.pontus-x.eu"

    def get_asset_owner(self, asset_did: str) -> str:
        """Queries the Aquarius cache API for the owner of an asset.

        Args:
            asset_did (str): The DID of the asset.

        Returns:
            str: The address of the asset owner.

        Raises:
            AssertionError: If the request to Aquarius fails or returns an error.
        """

        url = f"{self.url}/api/aquarius/assets/ddo/{asset_did}"
        res = requests.get(url)

        assert res.status_code == 200, f"Error querying Aquarius: {res.text}"

        return res.json().get("nft").get("owner")


aquarius = AquariusService()

__all__ = ["aquarius"]
