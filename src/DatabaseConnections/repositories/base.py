from abc import ABC, abstractmethod

from typing import List, Optional, Any


class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def create(self, entity: Any) -> None:
        pass

    @abstractmethod
    def update(self, entity: Any) -> None:
        pass

    @abstractmethod
    def delete(self, entity: Any) -> None:
        pass


class BaseRepository(AbstractRepository, ABC):
    @abstractmethod
    def execute_query(
        self, query: str, parameters: Optional[List[Any]] = None
    ) -> List[Any]:
        raise NotImplementedError()

    @abstractmethod
    def is_stable(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _get_connection_string(self) -> str:
        raise NotImplementedError()


class BaseReadOnlyRepository(BaseRepository):
    def get_by_id(self, entity_id: int) -> None:
        raise NotImplementedError("Create operation is not allowed.")

    def create(self, entity: Any) -> None:
        raise NotImplementedError("Create operation is not allowed.")

    def update(self, entity: Any) -> None:
        raise NotImplementedError("Update operation is not allowed.")

    def delete(self, entity: Any) -> None:
        raise NotImplementedError("Delete operation is not allowed.")
