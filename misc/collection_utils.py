# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from typing import Dict, List, Any

def without_keys(d: Dict[str,Any], *keys) -> Dict[str, Any]:
    return {k: v for k, v in d.items() if k not in keys}