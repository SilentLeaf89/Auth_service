import uuid

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode,
    # поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps

        allow_population_by_field_name = True

        json_encoders = {
            uuid.UUID: lambda u: str(u),
        }

    def get_search_fields(self) -> list[str]:
        pass

    def get_sort_fields(self) -> dict[str, str]:
        pass
