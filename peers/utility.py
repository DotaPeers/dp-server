import Config


def getProfilePicturePath(accountId):
    """
    Used to split filenames into subdirectories to prevent having one directory with too many files.
    """

    id_str = str(accountId)
    a = id_str[0]
    b = id_str[1]

    return f'{Config.PROFILE_PICTURES_FOLDER}/{a}/{b}/{accountId}.png'
