

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

    def __init__(self, type, userId):
        self.type = type
        if type == 1:
            self.msg = f"No connection for user ID {userId} found."
        elif type == 2:
            self.msg = f"Multiple connections for user ID {userId} found."
        else:
            self.msg = f"Invalid ConnectionError type {self.type}."

    def __str__(self):
        return f"{self.msg} ({self.type})"


class PlayerNotExistError(RuntimeError):

    def __init__(self, accountId):
        self.accountId = accountId

    def __str__(self):
        return f"No player exists for the account Id {self.accountId}"

