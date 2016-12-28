#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is mostly PEP8-compliant. See
# http://www.python.org/dev/peps/pep-0008/.

from dm.base import DialogueManager
from dm.exceptions import DMException


def get_dm_type(cfg):
    return cfg['DM']['type']


def dm_factory(dm_type, cfg):
    dm = None

    if dm_type == None:
        dm_type = get_dm_type(cfg)

    # do not forget to maintain all supported dialogue managers
    if dm_type == 'basic':  # 仅仅支持basic模式
        dm = DialogueManager(cfg)
    else:
        try:
            dm = dm_type(cfg)
        except NameError:
            raise DMException('Unsupported dialogue manager: %s' % dm_type)

    return dm
