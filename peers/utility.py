from typing import Union
from pathlib import Path
import io
import contextlib
import Config


def _splitAcountId(accountId):
    """
    Used to split filenames into subdirectories to prevent having one directory with too many files.
    """

    id_str = str(accountId)
    a = id_str[0]
    b = id_str[1]

    return f'{a}/{b}'


def getProfilePicturePath(accountId):
    """
    Path to the profile picture
    """

    dirs = _splitAcountId(accountId)

    return f'{Config.PROFILE_PICTURES_FOLDER}/{dirs}/{accountId}.png'


def getGraphPath(accountId):
    """
    Path to the profile graph
    """

    dirs = _splitAcountId(accountId)

    return f'{Config.GRAPH_PATHS}/{dirs}/{accountId}.html'


@contextlib.contextmanager
def safeOpen(path, mode='r') -> Union[io.TextIOWrapper, io.BufferedReader]:
    """
    Version of open(...), which creates the directory if it doesn't exist
    """

    file = None
    try:
        try:
            file = open(path, mode)
        except FileNotFoundError:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            file = open(path, mode)
        yield file

    finally:
        file.close()
