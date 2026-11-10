"""Herbruikbare API-client voor het abstraheren van API calls. Contract-achtig idee."""

from dataclasses import dataclass, field
from typing import Any

import requests


@dataclass
class ApiClient:
    """Een basis-url met standaardparameters en herbruikbare sessie."""

    base_url: str
    default_params: dict[str, Any] = field(default_factory=dict)
    timeout: float = 60.0
    session: requests.Session = field(default_factory=requests.Session)

    def get(self, path: str = "", **params: Any) -> Any:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        response = self.session.get(
            url, params={**self.default_params, **params}, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def post(self, path: str = "", json: Any = None) -> Any:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        response = self.session.post(url, json=json, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
