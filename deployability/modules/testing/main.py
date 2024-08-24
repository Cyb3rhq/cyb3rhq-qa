# Copyright (C) 2015, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import argparse
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

from modules.testing import Tester, InputPayload


def parse_arguments():
    parser = argparse.ArgumentParser(description="Cyb3rhq testing tool")
    parser.add_argument("--targets", action='append', default=[], required=True)
    parser.add_argument("--tests", required=True)
    parser.add_argument("--component", choices=['manager', 'agent', 'central_components'], required=True)
    parser.add_argument("--dependencies", action='append', default=[], required=False)
    parser.add_argument("--cleanup", required=False, default=True)
    parser.add_argument("--cyb3rhq-version", required=True)
    parser.add_argument("--cyb3rhq-revision", required=True)
    parser.add_argument("--cyb3rhq-branch", required=False)
    parser.add_argument("--live", required=False, default=False)

    return parser.parse_args()

if __name__ == "__main__":
    Tester.run(InputPayload(**vars(parse_arguments())))
