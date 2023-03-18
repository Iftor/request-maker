from urllib.parse import urljoin

import requests
from requests import RequestException

from app import settings
from app.db.models import QueueResponse, QueueRequest

CREDENTIALS = settings.REQUEST_LOGIN, settings.REQUEST_PASSWORD
CREDENTIALS = CREDENTIALS if all(CREDENTIALS) else None


def make_request(request_data: QueueRequest) -> QueueResponse | None:
    try:
        response = requests.request(
            method=request_data.method,
            url=urljoin(settings.REQUEST_URL, request_data.uri),
            params=request_data.params,
            headers=request_data.headers,
            timeout=settings.TIMEOUT,
            auth=CREDENTIALS
        )
        queue_response = QueueResponse(
            status_code=response.status_code,
            body=response.content.decode(),
            queue_request_id=request_data.id,
        )
        return queue_response
    except RequestException:
        return None
