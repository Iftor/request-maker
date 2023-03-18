from concurrent.futures import ThreadPoolExecutor
from app import settings
from app.db.accessors import QueueRequestAccessor, QueueResponseAccessor
from app.db.models import QueueResponse, QueueRequest
from app.src.utils import make_request


class RequestService:
    """Сервис S1 для выполнения запросов"""

    @staticmethod
    def _get_requests_data() -> list[QueueRequest]:
        """Получить данные о запросах"""

        return QueueRequestAccessor.get_requests_data()

    @staticmethod
    def _make_requests(requests_data: list[QueueRequest]) -> list[QueueResponse]:
        """
        Сделать запросы к сервису S2
        Многопоточный режим задается в настройках
        """

        if settings.MULTITHREADING:
            with ThreadPoolExecutor(len(requests_data)) as executor:
                queue_responses = executor.map(make_request, requests_data)
        else:
            queue_responses = map(make_request, requests_data)
        return list(filter(None, queue_responses))

    @staticmethod
    def _save_responses_data(responses_data: list[QueueResponse]) -> int:
        """Сохранить полученные данные ответов"""

        return QueueResponseAccessor.create_responses_data(responses_data) or 0

    @classmethod
    def run(cls) -> int:
        """
        API для доступа к сервису
        Выполняет последовательность всех действий
        """

        requests_data = cls._get_requests_data()
        if not requests_data:
            return 0
        responses_data = cls._make_requests(requests_data)
        if not responses_data:
            return 0
        return cls._save_responses_data(responses_data)
