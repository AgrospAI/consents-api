import logging
from dataclasses import dataclass, field

import requests
from helpers.config import config


@dataclass(frozen=True)
class AquariusService:

    url: str = field(default_factory=lambda: config.AQUARIUS_URL)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))

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
        self.logger.debug("Querying Aquarius at %s for asset owner.", url)

        res = requests.get(url)

        assert res.status_code == 200, f"Error querying Aquarius: {res.text}"
        return res.json().get("nft").get("owner")

    def get_asset_chain_id(self, asset_did: str) -> int:
        """Queries the Aquarius cache API for the chainId of an asset.

        Args:
            asset_did (str): The DID of the asset.

        Returns:
            int: The asset's chainId
        """

        url = f"{self.url}/api/aquarius/assets/ddo/{asset_did}"
        self.logger.debug("Querying Aquarius at %s for asset chainId.", url)

        res = requests.get(url)

        assert res.status_code == 200, f"Error querying Aquarius: {res.text}"
        return res.json().get("chainId")


aquarius = AquariusService()

__all__ = ["aquarius"]
