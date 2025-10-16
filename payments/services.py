from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PaymentIntent:
    provider: str
    external_id: str
    three_ds_required: bool
    redirect_url: Optional[str] = None
    payload: Dict[str, Any] = None


class PaymentService:
    """Provider-agnostic service interface."""

    def create_intent(self, order, totals: Dict[str, Any], return_urls: Dict[str, str], metadata: Dict[str, Any]) -> PaymentIntent:
        raise NotImplementedError

    def capture(self, payment, amount: Optional[str] = None) -> bool:
        raise NotImplementedError

    def refund(self, payment, amount: str, reason: str = "") -> bool:
        raise NotImplementedError

    def verify_webhook(self, request) -> Dict[str, Any]:
        """Return dict: {"valid": bool, "provider": str, "event_type": str, "dedupe_key": str, "payload": dict}"""
        raise NotImplementedError


class IyzicoSandboxAdapter(PaymentService):
    """IyziCo sandbox adapter skeleton. Real API calls will be added with credentials."""

    def __init__(self, api_key: str, secret: str, base_url: str):
        self.api_key = api_key
        self.secret = secret
        self.base_url = base_url

    def create_intent(self, order, totals: Dict[str, Any], return_urls: Dict[str, str], metadata: Dict[str, Any]) -> PaymentIntent:
        # TODO: integrate iyzico initialize 3DS checkout form
        return PaymentIntent(
            provider="iyzico",
            external_id=f"sandbox-{order.id}",
            three_ds_required=True,
            redirect_url=return_urls.get("success"),
            payload={"amount": str(totals.get("grand_total"))},
        )

    def capture(self, payment, amount: Optional[str] = None) -> bool:
        # TODO: call iyzico capture/approve if deferred
        return True

    def refund(self, payment, amount: str, reason: str = "") -> bool:
        # TODO: call iyzico refund endpoint
        return True

    def verify_webhook(self, request) -> Dict[str, Any]:
        # TODO: verify HMAC signature and parse event
        return {"valid": True, "provider": "iyzico", "event_type": "sandbox", "dedupe_key": request.headers.get("X-Event-Id", "sandbox"), "payload": {}}



