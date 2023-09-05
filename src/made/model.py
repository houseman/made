from __future__ import annotations

import re
import typing as t

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field

import typing_extensions as te

from . import error as err

if t.TYPE_CHECKING:
    from . import schema as s


class AbstractBaseModel(ABC):
    @abstractmethod
    def validate(self) -> te.Self:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(source: t.Any) -> AbstractBaseModel:  # TODO: Get rid of `Any`
        pass


@dataclass
class BaseModel(AbstractBaseModel):
    def validate(self) -> te.Self:
        return self

    def _validate_required_attrs(self, attrs: set[str | tuple[str, ...]]) -> None:
        _dict = asdict(self)
        _name = self.__class__.__name__
        for attr in attrs:
            if isinstance(attr, str):
                if not _dict.get(attr):
                    raise err.SchemaError(
                        f"{_name} requires a '{attr}' attribute: Found {_dict}"
                    )
            if isinstance(attr, tuple):
                if not any(iter(_dict.get(a) for a in attr)):
                    raise err.SchemaError(
                        f"{_name} requires one of '{', '.join(attr)}' attribute: "
                        f"Found {_dict}"
                    )

        return None


@dataclass
class VarModel(BaseModel):
    id: str
    value: str

    def validate(self) -> te.Self:
        self._validate_required_attrs({"id", "value"})

        return self

    @staticmethod
    def from_dict(source: s.VarSchema) -> VarModel:
        return VarModel(id=source["id"], value=source["value"]).validate()


@dataclass
class JobModel(BaseModel):
    id: str
    help: str | None = None
    run: str | None = None
    jobs: dict[str, JobModel] = field(default_factory=dict)
    args: list[str] = field(default_factory=list)

    def validate(self) -> te.Self:
        self._validate_required_attrs({"id", ("run", "jobs")})

        return self

    def _validate_args(self, var_keys: list[str]) -> None:
        for arg in self.args:
            match = re.search(r"\$\{(.*?)\}", arg)
            if match:
                var = match.group(1)
                if var not in var_keys:
                    raise err.VarError(f"Variable '{var}' is not defined")

        return None

    @staticmethod
    def from_dict(source: s.JobSchema) -> JobModel:
        return JobModel(
            id=source["id"],
            help=source.get("help"),
            run=source.get("run"),
            args=source.get("args", []),
            jobs={js["id"]: JobModel.from_dict(js) for js in source.get("jobs", [])},
        ).validate()


JobModelCollection: te.TypeAlias = dict[str, JobModel]
VarModelCollection: te.TypeAlias = dict[str, VarModel]


@dataclass
class MadeModel(BaseModel):
    vars: VarModelCollection
    jobs: JobModelCollection

    def validate(self) -> te.Self:
        for job in self.jobs.values():
            job._validate_args(list(self.vars.keys()))
        return self

    @staticmethod
    def from_dict(source: s.MadeSchema) -> MadeModel:
        return MadeModel(
            vars={vs["id"]: VarModel.from_dict(vs) for vs in source.get("vars", [])},
            jobs={js["id"]: JobModel.from_dict(js) for js in source.get("jobs", [])},
        ).validate()
