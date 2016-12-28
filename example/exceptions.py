'''
各种异常处理
'''


class AlexException(Exception):
    pass


class HubException(AlexException):
    pass


class SemHubException(HubException):
    pass


class TextHubException(HubException):
    pass


class VoipHubException(HubException):
    pass
