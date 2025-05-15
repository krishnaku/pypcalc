# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from sim.model import Registry
from .base import CollaboratorBase

collaborator_registry: Registry[CollaboratorBase] = Registry()
