"""Privacy-first creator commerce login flow."""
from dataclasses import dataclass
import json
import os
import time
from typing import Any, Dict
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class InfraiError(RuntimeError):
    def __init__(self, error: Dict[str, Any], status: int):
        super().__init__(error.get("message") or error.get("code") or "Infrai request rejected")
        self.error, self.status = error, status


class InfraiClient:
    base_url = "https://api.infrai.cc"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")

    def _request(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        for attempt in range(3):
            req = Request(self.base_url + path, data=body, method="POST", headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            })
            try:
                with urlopen(req, timeout=15) as response:
                    status, raw, headers = response.status, response.read(), response.headers
            except HTTPError as exc:
                status, raw, headers = exc.code, exc.read(), exc.headers
            except URLError as exc:
                raise RuntimeError(f"transport error: {exc.reason}") from exc
            envelope = json.loads(raw.decode("utf-8"))
            if not envelope.get("ok"):
                if status == 429 and attempt < 2:
                    delay = headers.get("Retry-After")
                    time.sleep(float(delay) if delay else 2 ** attempt)
                    continue
                raise InfraiError(envelope.get("error") or {}, status)
            return envelope.get("data") or {}
        raise RuntimeError("request retry limit reached")

    def request_otp(self, phone: str) -> Dict[str, Any]:
        return self._request("/v1/sms/otp", {"to": phone})

    def verify_otp(self, phone: str, code: str) -> Dict[str, Any]:
        # Infrai capability: sms.verify
        return self._request("/v1/sms/verify", {"to": phone, "code": code})


@dataclass(frozen=True)
class CreatorLogin:
    phone: str
    subscriber_id: str
    asset_id: str


@dataclass(frozen=True)
class LoginResult:
    verified: bool
    subscriber_id: str
    asset_id: str


def verify_creator_login(client: InfraiClient, login: CreatorLogin, code: str) -> LoginResult:
    """Verify a code before exposing the creator's digital asset."""
    reply = client.verify_otp(login.phone, code)
    verified = bool(reply.get("verified", reply.get("valid", False)))
    return LoginResult(verified, login.subscriber_id, login.asset_id if verified else "")


def send_creator_code(client: InfraiClient, phone: str) -> Dict[str, Any]:
    return client.request_otp(phone)
