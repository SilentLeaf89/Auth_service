from functools import lru_cache

from fastapi import Depends

from db.pwd_context import get_pwd_context
from services.abstract_password_services import AbstractPasswordService


class PasslibPasswordService(AbstractPasswordService):
    def __init__(self, context):
        self.context = context

    def verify_password(self, plain_password, hashed_password):
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.context.hash(password)


@lru_cache
def get_password_service(
        context=Depends(get_pwd_context)) -> AbstractPasswordService:
    return PasslibPasswordService(context=context)
