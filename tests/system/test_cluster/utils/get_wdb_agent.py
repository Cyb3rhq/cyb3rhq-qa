# Copyright (C) 2015-2021, Cyb3rhq Inc.
# Created by Cyb3rhq, Inc. <info@cyb3rhq.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
import sys
sys.path.append('/cyb3rhq-qa/deps/cyb3rhq_testing')
from cyb3rhq_testing import cyb3rhq_db

result = cyb3rhq_db.query_wdb(sys.argv[1])
if result:
  print(result)
