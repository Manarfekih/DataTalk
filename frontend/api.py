from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()


API_URL = os.getenv("DATA_TALK_API_URL", "http://127.0.0.1:8000")


class DataTalkAPI:
    def __init__(
        self,
        base_url: str = API_URL,
    ) -> None:
        self.base_url = base_url.rstrip("/")

    def _request_json(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = requests.request(
                method,
                f"{self.base_url}{path}",
                **kwargs,
            )
        except (requests.ConnectionError, requests.Timeout) as exc:
            raise RuntimeError(
                f"Could not reach the backend at {self.base_url}. "
                "Make sure the API server is running and the URL is correct."
            ) from exc

        response.raise_for_status()
        return response.json()

    def health(self) -> dict[str, Any]:
        return self._request_json(
            "GET",
            "/health",
            timeout=30,
        )

    def ask(self, question: str) -> dict[str, Any]:
        return self._request_json(
            "POST",
            "/query",
            json={"question": question},
            timeout=120,
        )

    def get_traces(self) -> list[dict[str, Any]]:
        return self._request_json("GET", "/observability/traces", timeout=30)

    def get_executions(self) -> list[dict[str, Any]]:
        return self._request_json("GET", "/observability/executions", timeout=30)

    def get_stats(self) -> dict[str, Any]:
        return self._request_json("GET", "/observability/stats", timeout=30)

    def get_evaluation(self) -> dict[str, Any]:
        return self._request_json("GET", "/observability/evaluation", timeout=30)

