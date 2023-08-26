from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, TypedDict, Any
from pprint import pformat
import yaml


class BaseSchemaSource(TypedDict):
    pass


class VarSchemaSource(BaseSchemaSource):
    id: str
    value: str


class JobSchemaSource(BaseSchemaSource):
    id: str
    run: str
    requires: list[str]
    args: list[str]
    vars: list[str]
    jobs: list[JobSchemaSource]


class MadeSchemaSource(BaseSchemaSource):
    vars: list[VarSchemaSource]
    jobs: list[JobSchemaSource]


class AbstractBaseSchema(ABC):
    @abstractmethod
    def validate(self) -> Self:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(source: Any) -> AbstractBaseSchema:
        pass


class BaseSchema(AbstractBaseSchema):
    def validate(self) -> Self:
        return self


@dataclass
class VarSchema(BaseSchema):
    id: str
    value: str

    @staticmethod
    def from_dict(source: VarSchemaSource) -> VarSchema:
        return VarSchema(id=source["id"], value=source["value"]).validate()


@dataclass
class JobSchema(BaseSchema):
    id: str
    jobs: dict[str, JobSchema]
    requires: list[str]
    args: list[str]

    @staticmethod
    def from_dict(source: JobSchemaSource) -> JobSchema:
        return JobSchema(
            id=source["id"],
            requires=source.get("requires", []),
            args=source.get("args", []),
            jobs={js["id"]: JobSchema.from_dict(js) for js in source.get("jobs", [])},
        ).validate()


@dataclass
class MadeSchema(BaseSchema):
    vars: dict[str, VarSchema]
    jobs: dict[str, JobSchema]

    @staticmethod
    def from_dict(source: MadeSchemaSource) -> MadeSchema:
        return MadeSchema(
            vars={vs["id"]: VarSchema.from_dict(vs) for vs in source.get("vars", [])},
            jobs={js["id"]: JobSchema.from_dict(js) for js in source.get("jobs", [])},
        ).validate()


if __name__ == "__main__":
    with open("../made-file.yaml") as made_file:
        made_config = yaml.safe_load(made_file)

    print(made_config)
    schema = MadeSchema.from_dict(made_config)
    print(f"schema: {pformat(schema)}")
