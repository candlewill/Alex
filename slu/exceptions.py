#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
各种异常处理
'''


class AlexException(Exception):
    pass


class ConfusionNetworkException(Exception):
    pass


class SLUException(AlexException):
    pass


class SLUConfigurationException(SLUException):
    pass


class DAILRException(SLUException):
    pass


class CuedDialogueActError(SLUException):
    pass


class DAIKernelException(SLUException):
    pass


class DialogueActItemException(SLUException):
    pass


class DialogueActException(SLUException):
    pass


class DialogueActNBListException(SLUException):
    pass


class DialogueActConfusionNetworkException(SLUException, ConfusionNetworkException):
    pass
