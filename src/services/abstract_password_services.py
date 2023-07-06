from abc import ABC, abstractmethod


class AbstractPasswordService(ABC):
    def __init__(self, context):
        self.context = context

    @abstractmethod
    def verify_password(
            self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        pass
