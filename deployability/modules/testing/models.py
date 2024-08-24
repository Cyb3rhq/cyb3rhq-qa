# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2
from typing import Literal

from pydantic import BaseModel, field_validator

class ExtraVars(BaseModel):
    """Extra vars for testing module."""
    component: Literal['manager', 'agent', 'central_components']
    cyb3rhq_version: str
    cyb3rhq_revision: str
    cyb3rhq_branch: str | None = None
    working_dir: str = '/tmp/tests'
    live: bool = False

class InputPayload(ExtraVars):
    """Input payload for testing module."""
    tests: list[str]
    targets: list[str]
    dependencies: list[str] | None = None
    cleanup: bool = True
    live: bool = False


    @field_validator('tests', mode='before')
    def validate_tests(cls, value) -> list[str]:
        """Validate tests names."""
        if type(value) is str:
            value = value.split(',')

        return value
