from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Self, Any, TypeAlias

from made.schema.source import VarSchemaSource, JobSchemaSource, MadeSchemaSource
from made.error import SchemaError, VarError


class AbstractBaseSchema(ABC):
    @abstractmethod
    def validate(self) -> Self:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(source: Any) -> AbstractBaseSchema:  # TODO: Get rid of `Any`
        pass


@dataclass
class BaseSchema(AbstractBaseSchema):
    def validate(self) -> Self:
        return self

    def _validate_required_attrs(self, attrs: set[str | tuple[str, ...]]) -> None:
        _dict = asdict(self)
        _name = self.__class__.__name__
        for attr in attrs:
            if isinstance(attr, str):
                if not _dict.get(attr):
                    raise SchemaError(
                        f"{_name} requires a '{attr}' attribute: Found {_dict}"
                    )
            if isinstance(attr, tuple):
                if not any(iter(_dict.get(a) for a in attr)):
                    raise SchemaError(
                        f"{_name} requires one of '{', '.join(attr)}' attribute: "
                        f"Found {_dict}"
                    )

        return None


@dataclass
class VarSchema(BaseSchema):
    id: str
    value: str

    def validate(self) -> Self:
        self._validate_required_attrs({"id", "value"})

        return self

    @staticmethod
    def from_dict(source: VarSchemaSource) -> VarSchema:
        return VarSchema(id=source["id"], value=source["value"]).validate()


@dataclass
class JobSchema(BaseSchema):
    id: str
    help: str | None = None
    run: str | None = None
    jobs: dict[str, JobSchema] = field(default_factory=dict)
    args: list[str] = field(default_factory=list)

    def validate(self) -> Self:
        self._validate_required_attrs({"id", ("run", "jobs")})

        return self

    def _validate_args(self, var_keys: list[str]) -> None:
        for arg in self.args:
            match = re.search(r"\$\{(.*?)\}", arg)
            if match:
                var = match.group(1)
                if var not in var_keys:
                    raise VarError(f"Variable '{var}' is not defined")

        return None

    @staticmethod
    def from_dict(source: JobSchemaSource) -> JobSchema:
        return JobSchema(
            id=source["id"],
            help=source.get("help"),
            run=source.get("run"),
            args=source.get("args", []),
            jobs={js["id"]: JobSchema.from_dict(js) for js in source.get("jobs", [])},
        ).validate()


JobCollection: TypeAlias = dict[str, JobSchema]
VarCollection: TypeAlias = dict[str, VarSchema]


@dataclass
class MadeSchema(BaseSchema):
    vars: VarCollection
    jobs: JobCollection

    def validate(self) -> Self:
        for job in self.jobs.values():
            job._validate_args(list(self.vars.keys()))
        return self

    @staticmethod
    def from_dict(source: MadeSchemaSource) -> MadeSchema:
        return MadeSchema(
            vars={vs["id"]: VarSchema.from_dict(vs) for vs in source.get("vars", [])},
            jobs={js["id"]: JobSchema.from_dict(js) for js in source.get("jobs", [])},
        ).validate()
