from pydantic import BaseModel
from typing import Dict, List


class PaymentCapturedPayload(BaseModel):
    entity: str
    account_id: str
    event: str
    contains: List[str]
    payload: Dict
