from typing import Any

from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:

        object_id_schema = core_schema.is_instance_schema(ObjectId)

        string_schema = core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

        return core_schema.union_schema(
            [
                object_id_schema,
                string_schema,
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda value: str(value),
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def validate(cls, value: str) -> "PyObjectId":
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return cls(value)