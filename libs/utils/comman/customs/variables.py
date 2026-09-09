from collections.abc import Mapping
from typing import Any, Literal

from bson import ObjectId
from pydantic import BaseModel, GetCoreSchemaHandler, model_validator
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
                cls.serialize,
                return_schema=core_schema.str_schema(),
                when_used="json",
            ),
        )

    @classmethod
    def validate(cls, value: str) -> "PyObjectId":
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return cls(value)

    @staticmethod
    def serialize(value: ObjectId) -> str:
        return str(value)


class MongoBaseModel(BaseModel):
    """Normalize MongoDB _id values to the public id field."""

    @model_validator(mode="before")
    @classmethod
    def normalize_id(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            value = dict(value)
            if "_id" in value and "id" not in value:
                value["id"] = value.pop("_id")
        return value

    def model_dump(
        self,
        *,
        mode: Literal["python", "json", "Json", "ObjectId"] = "python",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Dump with optional JSON or MongoDB ID conventions.

        The default Python dump preserves the model field name and value.
        "Json" emits ``id`` and JSON-compatible string IDs. "ObjectId"
        emits ``_id`` and BSON ObjectId values for MongoDB writes.
        """
        if mode == "Json":
            return super().model_dump(mode="json", **kwargs)

        if mode == "ObjectId":
            data = super().model_dump(mode="python", **kwargs)
            return self._as_mongodb_document(data)

        return super().model_dump(mode=mode, **kwargs)

    @classmethod
    def _as_mongodb_document(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            result = {}
            for key, item in value.items():
                if key == "id":
                    result["_id"] = cls._as_object_id(item)
                else:
                    result[key] = cls._as_mongodb_document(item)
            return result
        if isinstance(value, list):
            return [cls._as_mongodb_document(item) for item in value]
        return value

    @staticmethod
    def _as_object_id(value: Any) -> ObjectId:
        if isinstance(value, ObjectId):
            return value
        return PyObjectId.validate(value)
