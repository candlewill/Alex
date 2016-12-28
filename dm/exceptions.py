#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
各种异常处理
'''


class AlexException(Exception):
    pass


class DMException(AlexException):
    pass


class DialogueStateException(AlexException):
    pass


class DialoguePolicyException(AlexException):
    pass


class DialogueManagerException(AlexException):
    pass


class DeterministicDiscriminativeDialogueStateException(DialogueStateException):
    pass


class DummyDialoguePolicyException(DialoguePolicyException):
    pass
