from sqlalchemy import select, update, Update

from app.db.models import (
    QueueResponseModel,
    QueueRequestModel,
    QueueRequest,
    QueueResponse,
)
from app.db.session import Session


class QueueRequestAccessor:
    """Аксессор для взаимодействия с таблицей запросов в бд"""

    @staticmethod
    def get_requests_data() -> list[QueueRequest]:
        """Получить данные о запросах из бд"""

        with Session() as session:
            queue_requests = session.scalars(
                select(QueueRequestModel).filter(QueueRequestModel.processed == False)
            )
            return [queue_request.dataclass for queue_request in queue_requests if queue_request.dataclass]

    @staticmethod
    def get_delete_requests_query(queue_requests_ids: list[int]) -> Update:
        """Сформировать запрос soft-удаления из бд обработанных запросов"""

        query = update(
            QueueRequestModel
        ).filter(
            QueueRequestModel.id.in_(queue_requests_ids)
        ).values(processed=1)
        return query


class QueueResponseAccessor:
    """Аксессор для взаимодействия с таблицей ответов в бд"""

    @staticmethod
    def create_responses_data(queue_responses: list[QueueResponse]) -> int | None:
        """Создать записи в бд о полуенных ответах"""

        with Session() as session:
            session.add_all([
                QueueResponseModel(
                    status_code=queue_response.status_code,
                    body=queue_response.body,
                    queue_request_id=queue_response.queue_request_id,
                ) for queue_response in queue_responses
            ])
            delete_requests_query = QueueRequestAccessor.get_delete_requests_query(
                [queue_response.queue_request_id for queue_response in queue_responses]
            )
            session.execute(delete_requests_query)
            session.commit()
        return len(queue_responses)
