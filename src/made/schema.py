from __future__ import annotations

from typing import TypedDict


class BaseSchema(TypedDict):
    pass


class VarSchema(BaseSchema):
    id: str
    value: str


class JobSchema(BaseSchema):
    id: str
    help: str
    run: str
    args: list[str]
    jobs: list[JobSchema]


class MadeSchema(BaseSchema):
    vars: list[VarSchema]
    jobs: list[JobSchema]
