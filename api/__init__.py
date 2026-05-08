"""API 클라이언트 팩토리 — USE_MOCK_API=false 시 실제 API로 전환."""

import os

_use_mock = os.getenv("USE_MOCK_API", "true").lower() != "false"

if _use_mock:
    from api.mock_clients import MockETRIClient, MockEICTClient, MockSookmyungClient
    etri_client = MockETRIClient()
    eict_client = MockEICTClient()
    sookmyung_client = MockSookmyungClient()
else:
    from api.etri_client import ETRIClient
    from api.eict_client import EICTClient
    from api.sookmyung_client import SookmyungClient
    etri_client = ETRIClient()
    eict_client = EICTClient()
    sookmyung_client = SookmyungClient()

__all__ = ["etri_client", "eict_client", "sookmyung_client"]
