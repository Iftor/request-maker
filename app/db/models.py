from dataclasses import dataclass
from json import JSONDecodeError

from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, ColumnDefault
from sqlalchemy.orm import declarative_base
import json
from urllib.parse import urljoin

from app import settings

Base = declarative_base()


@dataclass
class QueueRequest:
    id: int
    uri: str
    method: str
    params: dict | None
    headers: dict | None


@dataclass
class QueueResponse:
    status_code: int
    body: str
    queue_request_id: int


class QueueRequestModel(Base):
    __tablename__ = "queue_requests"

    id = Column(Integer(), primary_key=True)
    uri = Column(String())
    method = Column(String(6), nullable=False)
    params = Column(String())
    headers = Column(String())
    processed = Column(Boolean(), ColumnDefault(False), server_default="0")

    @property
    def dataclass(self) -> QueueRequest | None:
        """Приводит объект модели к объекту датакласса или возвращает None в случае некорректных данных"""

        id_ = self.id
        uri = self.uri
        method = self.method
        try:
            params = json.loads(self.params) if self.params else None
            headers = json.loads(self.headers) if self.headers else None
        except JSONDecodeError:
            return None
        return QueueRequest(id_, uri, method, params, headers)

    def __repr__(self) -> str:
        return f'{self.method} {urljoin(settings.REQUEST_URL, self.uri)}'


class QueueResponseModel(Base):
    __tablename__ = "queue_responses"

    id = Column(Integer(), primary_key=True)
    status_code = Column(Integer(), nullable=False)
    body = Column(String(), nullable=False)
    queue_request_id = Column(Integer(), ForeignKey("queue_requests.id"))

    def __repr__(self) -> str:
        return f'{self.status_code} request_id: {self.queue_request_id}'
