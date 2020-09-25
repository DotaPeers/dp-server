

class InvalidChannelError(RuntimeError):

    def __init__(self, channelId, userId):
        self._channelId = channelId
        self._userId = userId


    @property
    def channelId(self):
        return self._channelId

    @property
    def userId(self):
        return self._userId

    def __str__(self):
        return f"Found invalid channel {self.channelId} for user {self.userId}."


class ConnectionError(RuntimeError):

    def __init__(self, msg, type):
        self.msg = msg
        self.type = type

    def __str__(self):
        return 'ConnectionError'
