# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from typing import Dict, List, Any

def without_keys(d: Dict[str,Any], *keys) -> Dict[str, Any]:
    return {k: v for k, v in d.items() if k not in keys}