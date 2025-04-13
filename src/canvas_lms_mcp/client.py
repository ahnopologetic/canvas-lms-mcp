from typing import Any, Dict, Optional

import httpx


class CanvasClient:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CanvasClient, cls).__new__(cls)
        return cls._instance

    def __init__(
        self, api_token: str = None, base_url: str = "https://canvas.instructure.com"
    ):
        # Only initialize once
        if not self._initialized and api_token is not None:
            self.api_token = api_token
            self.base_url = base_url
            self.client = httpx.AsyncClient(
                base_url=base_url,
                headers={
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json",
                },
            )
            self._initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError(
                "CanvasClient has not been initialized. Call CanvasClient(api_token) first."
            )
        return cls._instance

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a GET request to the Canvas API."""
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request to the Canvas API."""
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PUT request to the Canvas API."""
        response = await self.client.put(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request to the Canvas API."""
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return response.json()

    def close(self):
        """Close the HTTP client."""
        self.client.close()
