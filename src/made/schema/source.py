from __future__ import annotations

from typing import TypedDict


class BaseSchemaSource(TypedDict):
    pass


class VarSchemaSource(BaseSchemaSource):
    id: str
    value: str


class JobSchemaSource(BaseSchemaSource):
    id: str
    help: str
    run: str
    args: list[str]
    jobs: list[JobSchemaSource]


class MadeSchemaSource(BaseSchemaSource):
    vars: list[VarSchemaSource]
    jobs: list[JobSchemaSource]
